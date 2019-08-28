$(document).ready(function() {
  eventSource = new EventSource("/events/");
  eventSource.addEventListener('message', function (e) {
    message = e.data.replace('"', '').replace('\"', '');
    if (message == "uploading completed") {
      window.location.replace("/products");
    } else {
      $("#message").text(message);
    }
  });
  eventSource.addEventListener('stream-reset', function (e) {
    $("#message").text("Unknown error happen");
    window.location.replace("/products");
  }, false);
});
