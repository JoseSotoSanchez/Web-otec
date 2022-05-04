function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

$(document).ready(function() {
  // show the alert
  setTimeout(function() {
      $(".alert").alert('close');
  }, 4000);
});



$(document).ready(function() {
  $('ul.navbar-nav > li').removeClass('active');
  $('a[href="' + location.pathname + '"]').closest('li').addClass('active'); 
});

