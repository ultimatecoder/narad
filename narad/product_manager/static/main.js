$(document).ready(function() {
  eventSource = new EventSource("/events/");
  eventSource.addEventListener('message', function (e) {
    $("#message").text(e.data);
    console.log(e.data);
  });
});
