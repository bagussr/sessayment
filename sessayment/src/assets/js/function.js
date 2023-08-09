var nowLocation = window.location.href;
function onClick(route) {
  window.location.href = nowLocation + route;
}

function onBack() {
  window.history.back();
}
