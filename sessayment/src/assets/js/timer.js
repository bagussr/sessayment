import $ from 'jquery';

$(document).ready(function () {
  const startTime = new Date().getTime();
  const endTime = 3600000;
  const time = $('#startTime');
  var zero = 0;
  var width = 0;
  setInterval(setTime, 1000);
  $('#endTime').html(
    pad(parseInt(endTime / 3600000)) +
      ':' +
      pad(parseInt((endTime % 3600000) / 60000))
  );

  function setTime() {
    ++zero;
    const seconds = pad(zero % 60);
    const minutes = pad(parseInt(zero / 60));
    const currentTimestamp = new Date().getTime();

    time.html(minutes + ':' + seconds);
    if (width < 100) {
      width = ((currentTimestamp - startTime) / endTime) * 60 * 100;

      $('#distanceTime').css('width', Math.floor(width) + '%');
    } else {
      clearInterval(setTime);
      window.location.href =
        "{{ url_for('result_assesment', id=item, course='kuis 1') }}";
    }
  }

  function pad(val) {
    var valString = val + '';
    if (valString.length < 2) {
      return '0' + valString;
    } else {
      return valString;
    }
  }
});
