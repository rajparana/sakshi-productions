from pickle import GET
from django.shortcuts import render, redirect
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import *
from .forms import PostForm, SignUpForm, LogInForm

def home(request):
    cats = Category.objects.all()
    topQuote = TopQuote.objects.filter(status='Active').last()
    bottomQuote = BottomQuote.objects.filter(status='Active').last()
    collageCrousels = CollageCrousel.objects.filter(status='Active').all()[:11]
    slideCrousels = SlideCrousel.objects.filter(status='Active').all()[:11]
    weddings = Post.objects.filter(category__name='Wedding', published_date__lte=timezone.now(), status='Active').order_by('published_date')
    preWeddings = Post.objects.filter(category__name='Pre-Wedding', published_date__lte=timezone.now(), status='Active').order_by('published_date')
    reach = Reach.objects.filter(status='Active').last()
    images = Album.objects.filter(status='Active').all()[:15]
    testimonialCover = Testimonial.objects.filter(status='Hidden').last()
    testimonials = Testimonial.objects.filter(status='Active').all()

    context = {
        'cats': cats,
        'topQuote': topQuote,
        'bottomQuote': bottomQuote,
        'collageCrousels': collageCrousels,
        'slideCrousels': slideCrousels,
        'weddings': weddings,
        'preWeddings': preWeddings,
        'reach': reach,
        'images': images,
        'testimonialCover': testimonialCover,
        'testimonials': testimonials,
        }
    return render(request, 'sakshi/index.html', context)

def log_out(request):
    logout(request)
    return redirect(reverse('home'))

def log_in(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                # messages.success(request, 'You\'ve Successfully LogIn')
                return redirect('post_new')
            else:
                messages.error(request, 'User with this email not found, please register first.')
                return redirect('login')
        else:
            log_out(request)
            messages.error(request, 'Please Enter correct Email and Password!')
            return redirect('login')
    return render(request, 'sakshi/login.html', {})

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        mobile = request.POST.get('mobile', None)
        code = request.POST.get('code', None)
        password = request.POST.get('password', None)
        cpassword = request.POST.get('cpassword', None)

        if (email is None) or (first_name is None) or (mobile is None) or (password is None) or (cpassword is None) or (code is None):
            messages.error(request, 'All fields are required')
            return redirect('signup')

        if User.objects.filter(email=email).first():
            messages.error(request, 'User is exist with this Email')
            return redirect('signup')

        if User.objects.filter(mobile=mobile).first():
            messages.error(request, 'User is exist with this Mobile Number')
            return redirect('signup')

        if code != 124421:
            messages.error(request, 'Code is not correct')
            return redirect('signup')

        if password != cpassword:
            messages.error(request, 'Password is not matching')
            return redirect('signup')
        
        if first_name and email and mobile and password and cpassword:
            user = User.objects.create(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = email,
                mobile = mobile,
                password = password
            )
            
            if user:
                login(request, user)
                # messages.success(request, 'You\'ve Successfully SignUp')
                return redirect('post_new')
            else:
                messages.error(request, 'Something went wrong')
                return redirect('signup')
        else:
            messages.error(request, 'Please enter all details correctly')
            return redirect('signup')
    return render(request, 'sakshi/signup.html', {})

def post_detail(request, slug):
    cats = Category.objects.all()
    post = get_object_or_404(Post, slug=slug)
    album = Album.objects.filter(post=post).all()
    return render(request, 'sakshi/post_detail.html', {'cats':cats, 'post': post, 'album':album})

def post_list(request):
    cats = Category.objects.all()
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'sakshi/post_list.html', {'cats':cats, 'posts': posts})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            # post.thumbnail = request.FILES.get('thumbnail')
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            if request.FILES.getlist('album'):
                album = request.FILES.getlist('album')
                for image in album:
                    Album.objects.create(post=post, category=post.category, album=image)
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'sakshi/post_edit.html', {'form': form})

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            # if request.FILES.get('thumbnail'):
            #     post.thumbnail = request.FILES.get('thumbnail')
            post.save()
            if request.FILES.getlist('album'):
                album = request.FILES.getlist('album')
                for image in album:
                    Album.objects.create(post=post, category=post.category, album=image)
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'sakshi/post_edit.html', {'form': form})

def category(request, slug):
    cat = Category.objects.filter(slug=slug).last()
    posts = Post.objects.filter(category=cat).all()
    return render(request, 'sakshi/category_detail.html', {'cat': cat, 'posts': posts, 'num': posts.count()})

def portfolio(request):
    images = Album.objects.all()
    cats = Category.objects.all()
    return render(request, 'sakshi/portfolio.html', {'cats': cats,'images':images})

def contact(request):
    cats = Category.objects.all()
    contactUs = Contact.objects.filter(status='Active').last()
    return render(request, 'sakshi/contact.html', {'cats': cats, 'contactUs': contactUs})

def about(request):
    cats = Category.objects.all()
    topAbout = TopAbout.objects.filter(status='Active').last()
    midAbout= MidAbout.objects.filter(status='Active').last()
    bottomAbout = BottomAbout.objects.filter(status='Active').last()
    aboutQuote = AboutQuote.objects.filter(status='Active').last()
    services = Service.objects.filter(status='Active').all()[:6]
    expertises = Expertise.objects.filter(status='Active').all()[:4]
    context = {
        'cats': cats,
        'topAbout': topAbout,
        'midAbout': midAbout,
        'bottomAbout': bottomAbout,
        'aboutQuote': aboutQuote,
        'services': services,
        'expertises': expertises,
        }
    return render(request, 'sakshi/about.html', context)

# def tag(request, slug):
#     rfr = Tag.objects.filter(slug=slug).last()
#     posts = Post.objects.filter(tag=rfr).all()
#     return render(request, 'blog/tag_detail.html', {'posts': posts, 'rfr': rfr, 'num': posts.count()})