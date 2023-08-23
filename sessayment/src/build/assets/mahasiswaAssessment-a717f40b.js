import './index-b8dcdbd2.js';
import { $ } from './vendor-8b449814.js';
$(document).ready(function () {
  const id = location.pathname.split('/')[3];
  const assesmentStart = $('input[name=assesment_start]').val();
  const startTime = /* @__PURE__ */ new  Date().setHours(assesmentStart.split(':')[0], assesmentStart.split(':')[1], 0)
  const timeAssesment = $('input[name=time_assesment]').val()
  const endTime = 36e5 * timeAssesment;
  const time = $('#startTime');
  const end =new Date(endTime / 60 + new Date(startTime).getTime())
  const noSoal = $('#no_soal')
  const submit = $('#submit-assesment')


  var text_question = $('#answer')
  var zero = ((new Date(startTime).getTime() + new Date().getTime() - end.getTime())  % 36e5 / 1000).toFixed(0);
  var width = 0;


  setInterval(setTime, 1e3);
  $('#endTime').html(
    pad(end.getHours() - new Date(startTime).getHours() ) + ':' + pad(end.getMinutes()) + ':' + pad(end.getSeconds())
  );
  function setTime() {
    zero++;
    const seconds = pad((zero % 60));
    const minutes = pad(parseInt(zero / 60));
    const currentTimestamp = /* @__PURE__ */ new Date().getTime();
    const hours = pad(parseInt((currentTimestamp - new Date(startTime).getTime()) / 36e5 ));
    time.html(hours + ":" + minutes + ':' + seconds);
    if (width < 100) {
      width = ((currentTimestamp - startTime) / endTime) * 60 * 100;
      $('#distanceTime').css('width', Math.floor(width) + '%');
    } else {
      clearInterval(setTime);
      var data = window.localStorage.getItem('jawaban')
      $.ajax({
        method: 'POST',
        url: '/mahasiswa/assesment/' + id,
        data: {
          'jawaban': data
        },
        success: function (data) {},
        error: function (data) {},
      })
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

  var question = 0

  submit.on('click', function () {
    var data = window.localStorage.getItem('jawaban')
    if (data == undefined) {
      alert('Jawaban tidak boleh kosong')
    }
    $.ajax({
      method: 'POST',
      url: '/mahasiswa/assesment/' + id,
      data: {
        'jawaban': data
      },
      beforeSend: function () {
        window.localStorage.clear()
      },
      success: function (data) {
        window.location.href = data.url
      },
      error: function (data) {},
    })
  })

  get_question('/mahasiswa/assesment/' + id +`?question=${question}`, question)


  const next = $('#next_question');
  const prev = $('#prev_question');

  check_prev_next()

  next.on('click', function () {
    if (question+1 < noSoal.data('soal')){
      next.css('display', 'block')
      question++
      check_prev_next()
      get_question('/mahasiswa/assesment/' + id +`?question=${question}`, question)
    }
  })

  prev.on('click', function () {
    next.css('display', 'block')
    question--
    check_prev_next()
    get_question('/mahasiswa/assesment/' + id +`?question=${question}`, question)
  })

  text_question.change(function (e) {
    var jawaban = e.target.value
    var localStorage = window.localStorage.getItem('jawaban')
    if (localStorage != undefined) {
      var data = JSON.parse(localStorage)
      var temp = data.find(x => x.question_id == $(this).attr('data-jawaban'))
      if (temp != undefined) {
        temp.answer = jawaban
      } else{
        data.push({
          'question_id': $(this).attr('data-jawaban'),
          'answer': jawaban
        })
      }
      window.localStorage.setItem('jawaban', JSON.stringify(data))
    } else{
      var temp = []
      temp.push({
        'question_id': $(this).attr('data-jawaban'),
        'answer': jawaban
      })
      window.localStorage.setItem('jawaban', JSON.stringify(temp))
    }
  })


  function get_question(url, index) {
    var question = $('#question');
    var no_soal = $('#no_soal');
    text_question.attr('data-index', index)
    no_soal.html(index+1)
    $.ajax({
      method: 'GET',
      url: url,
      headers:{
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      success: function (data) {
        var x= data.data.question
        question.html(x[index].soal+ '?')
        text_question.attr('data-jawaban', x[index].id)
        check_local_answer(x[index].id)
      },
      error: function (data) {},
    });
  }

  function check_prev_next() {
    if (question == 0) {
      prev.css('display', 'none')
    } else {
      prev.css('display', 'block')
    }
  }

  function check_local_answer(id){
    var jawaban = window.localStorage.getItem('jawaban')
    if (jawaban != undefined){
      jawaban = JSON.parse(jawaban)
      var temp = jawaban.find(x => x.question_id == id)
      if (temp != undefined) {
        text_question.val(temp.answer)
      } else {
        text_question.val('')
      }
    }
  }
});


window.addEventListener('hashchange', function () {
  document.cookie = 'jawaban=[]'
})
