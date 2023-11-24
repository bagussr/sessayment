import './index-b8dcdbd2.js';
import { $ } from './vendor-8b449814.js';
$(document).ready(function () {
  const id = location.pathname.split('/')[3];
  const assesmentStart = $('input[name=assesment_start]').val();
  const startTime = /* @__PURE__ */ new Date().setHours(
    assesmentStart.split(':')[0],
    assesmentStart.split(':')[1],
    0
  );
  const timeAssesment = $('input[name=time_assesment]').val();
  const endTime = 36e5 * timeAssesment;
  const time = $('#startTime');
  const end = new Date(endTime / 60 + new Date(startTime).getTime());
  const noSoal = $('#no_soal');
  const submit = $('#submit-assesment');

  var text_question = $('#answer');
  var zero = (
    ((new Date(startTime).getTime() + new Date().getTime() - end.getTime()) %
      36e5) /
    1000
  ).toFixed(0);
  var width = 0;

  setInterval(setTime, 1e3);
  $('#endTime').html(
    pad(end.getHours() - new Date(startTime).getHours()) +
      ':' +
      pad(end.getMinutes()) +
      ':' +
      pad(end.getSeconds())
  );
  function setTime() {
    zero++;
    const seconds = pad(zero % 60);
    const minutes = pad(parseInt(zero / 60));
    const currentTimestamp = /* @__PURE__ */ new Date().getTime();
    const hours = pad(
      parseInt((currentTimestamp - new Date(startTime).getTime()) / 36e5)
    );
    time.html(hours + ':' + minutes + ':' + seconds);
    if (width < 100) {
      width = ((currentTimestamp - startTime) / endTime) * 60 * 100;
      $('#distanceTime').css('width', Math.floor(width) + '%');
    } else {
      clearInterval(setTime);
      var data = window.localStorage.getItem('jawaban');
      $.ajax({
        method: 'POST',
        url: '/mahasiswa/assesment/' + id,
        data: {
          jawaban: data,
        },
        success: function (data) {},
        error: function (data) {},
      });
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

  var question = 0;

  submit.on('click', function () {
    // post data to server from input[type=file]
    var formData = new FormData();
    var canvas = $('canvas');
    // var input = $('input[type=file]');
    for (var i = 0; i < canvas.length; i++) {
      formData.append(
        `file-${canvas[i].getAttribute('data-id')}`,
        canvas[i].toDataURL('image/png')
      );
    }
    $.ajax({
      method: 'POST',
      url: '/mahasiswa/assesment/' + id,
      data: formData,
      contentType: false,
      processData: false,
      beforeSend: function () {
        $('main').append(
          '<div class="loading-overlay"><div class="loading"><div class="loader"></div></div></div>'
        );
      },
      success: function (data) {
        window.location.href = data.url;
      },
    });
  });

  get_question(
    '/mahasiswa/assesment/' + id + `?question=${question}`,
    question
  );

  const next = $('#next_question');
  const prev = $('#prev_question');

  check_prev_next();

  next.on('click', function () {
    if (question + 1 < noSoal.data('soal')) {
      next.css('display', 'block');
      question++;
      get_question(
        '/mahasiswa/assesment/' + id + `?question=${question}`,
        question
      );
    }
  });

  prev.on('click', function () {
    next.css('display', 'block');
    question--;
    check_prev_next();
    get_question(
      '/mahasiswa/assesment/' + id + `?question=${question}`,
      question
    );
  });

  text_question.change('change', function (e) {
    console.log(e.target.value);
  });

  function get_question(url, index) {
    var question = $('#question');
    var no_soal = $('#no_soal');
    text_question.attr('data-index', index);
    no_soal.html(index + 1);
    $.ajax({
      method: 'GET',
      url: url,
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      success: function (data) {
        var x = data.data.question;
        question.html(x[index].soal + '?');
        var jawaban = $('#answer-' + x[index].id);
        jawaban.removeClass('hide');
        if (index > 0) {
          var prevJawaban = $('#answer-' + x[index - 1].id);
          prevJawaban.addClass('hide');
          var prevCanvas = $('#canvas-' + x[index - 1].id)[0];
          var prevCtx = prevCanvas.getContext('2d');
          prevCtx.clearRect(0, 0, 500, prevCanvas.height);
          prevCanvas.style.padding = '5px';
          prevCtx.fillStyle = '#fff';
          prevCtx.fillRect(0, 0, prevCanvas.width, prevCanvas.height);
          prevCtx.fillStyle = '#000';
          prevCtx.font = 'italic small-caps 32px cursive';
          prevCtx.fontKerning = 'none';
          prevCtx.letterSpacing = '5px';
          prevCtx.fillText(prevJawaban.value, 30, 50);
        }
        if (index == 0) {
          var nextJawaban = $('#answer-' + x[index + 1].id);
          nextJawaban.addClass('hide');
        }
        text_question.attr('data-jawaban', x[index].id);
        check_local_answer(x[index].id);
      },
      error: function (data) {},
    });
  }

  function check_prev_next() {
    if (question == 0) {
      prev.css('display', 'none');
    } else {
      prev.css('display', 'block');
    }
  }

  function check_local_answer(id) {
    var jawaban = window.localStorage.getItem('jawaban');
    if (jawaban != undefined) {
      jawaban = JSON.parse(jawaban);
      var temp = jawaban.find(x => x.question_id == id);
      if (temp != undefined) {
        text_question.val(temp.answer);
      } else {
        text_question.val('');
      }
    }
  }
});

window.addEventListener('hashchange', function () {
  document.cookie = 'jawaban=[]';
});
