/*
 * Show flash messages and FadeOut
 */
$(document).ready(function() {
  // Show flash messages
  $('.flash-message').each(function() {
      $(this).show().delay(5000).fadeOut();
  });
});

/*
 * Button to confirm the account deletion.
 * user should Enter their username.
 */
function confirmDeletion() {
  var username = prompt("Please enter your username to confirm deletion:");
  console.log("Entered username: " + username);
  console.log("Expected username: " + username)
  if (username === username) {
      document.getElementById("delete-form").submit();
  } else {
      alert("Incorrect username. Please try again.");
  }
}

