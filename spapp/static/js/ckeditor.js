$('#modal').html("<form><textarea id=foo></textarea></form>"); 

$('#modal').hide(); 
$('textarea#foo').ckeditor({ 
    height: "300px", 
    toolbarStartupExpanded: true, 
    width: "100%" 
}); 

$('#modal').hide(); 

window.setTimeout(function() { 
    $('#modal').show(); 
}, 3000); 
