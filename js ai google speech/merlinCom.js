
if (!('webkitSpeechRecognition' in window)) {

    const Toast = Swal.mixin({
        toast: true,
        position: "bottom-end",
        showConfirmButton: false,
        timer: 5000,
        timerProgressBar: true,
        didOpen: (toast) => {
          toast.onmouseenter = Swal.stopTimer;
          toast.onmouseleave = Swal.resumeTimer;
        }
      });
      Toast.fire({
        icon: "error",
        title: "<p dir='rtl' style='font-weight: normal; font-size: .8em;'>مرورگر شما از <span style='color:red;'>Web Speech API</span> پشتیبانی نمی کند. لطفاً این را در یک مرورگر پشتیبانی شده مانند گوگل‌کروم امتحان کنید.</p>"
      });
    // alert("Your browser doesn't support the Web Speech API. Please try this on a supported browser.");
} else {
    const startBtn = document.getElementById('startBtn')
    const stopBtn = document.getElementById('stopBtn')

    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true; // Keep listening for further commands
    recognition.interimResults = false;
    recognition.lang = 'fa-IR'; // Set language to Farsi

    recognition.onstart = function() {
        console.log('Voice recognition started.');
    };

    const responseContainer = document.getElementById('commentTextarea');
    recognition.onresult = function(event) {
        var resultText = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
            const result = event.results[i];
            resultText += result[0].transcript; // Add the transcript text
        }
        function showResponseCharByChar(response) {
            let i = 0;
            // responseContainer.innerHTML = ''; // Clear previous response
            responseContainer.value += ' ';
            
            
    //          // Replace in div
    //    response = response.replace(/نقطه/g, '.')
    //    .replace(/خط بعد/g, '\n')
    //    .replace(/دو ./g, ':')
    //    .replace(/دات/g, '.')
    //    .replace(/منهای/g, '-')
    //    .replace(/منها/g, '-')
    //    .replace(/بعلاوه /g, '+')
    //    .replace(/به علاوه /g, '+')
    //    .replace(/به علاوه/g, '+')
    //    .replace(/بعلاوه/g, '+')
    //    .replace(/جمع/g, '+')
    //    .replace(/تفریق/g, '-')
    //    .replace(/ضرب/g, '*')
    //    .replace(/تقسیم/g, '/')
    //    .replace(/تقسیم بر/g, '/')
    //    .replace(/ویرگول/g, ';')
    //    .replace(/کاما/g, '،')
    //    .replace(/شارپ/g, '#')
    //    .replace(/دلار/g, '$')
    //    .replace(/ستاره/g, '*')
    //    .replace(/پرانتز بسته/g, ')')
    //    .replace(/پرانتز باز/g, '(')
    //    .replace(/مساوی /g, '=')
    //    .replace(/برابر /g, '=')
    //    .replace(/درصد/g, '%')
    //    .replace(/علامت سوال/g, '؟')
    //    .replace(/علامت تعجب/g, '!')
    //    .replace(/تب/g, '    ')
    //    .replace(/اتساین/g, '@')
    //    .replace(/ایموجی بوس/g, '😘')
    //    .replace(/ایموجی قلب/g, '❤')
    //    .replace(/ایموجی هر هر/g, '😂')
    //    .replace(/ایموجی خشم/g, '😡')
    //    .replace(/ایموجی لایک/g, '👍')
    //    .replace(/دیس 👍/g, '👎')
    //    .replace(/ایموجی مشت/g, '👊')
    //    .replace(/ایموجی خنده/g, '😂')
    //    .replace(/'ایموجی گریه'/g, '😭');

       
    
            
            function typeWriter() {
                if (i < response.length) {
                    responseContainer.value += response.charAt(i);
                    i++;
                    setTimeout(typeWriter, 10); // Adjust typing speed here
                }
            }
            
            typeWriter();
        }
        showResponseCharByChar(resultText); // Put the result text in the textarea
        
        // respondToCommand(resultText);
        stopListening();
    };

    recognition.onerror = function(event) {
        console.error('Error occurred in recognition: ' + event.error);
    };

    recognition.onend = function() {
        console.log('Voice recognition ended.');
    };

    function startListening() {
        startBtn.hidden = true;
        stopBtn.hidden = false;
        recognition.start();
    }

    function stopListening() {
        startBtn.hidden = false;
        stopBtn.hidden = true;
        recognition.stop();
    }

    function reloadListening() {
        stopListening();
        // Small delay to ensure that the recognition has stopped
        setTimeout(() => {
            recognition.start();
        }, 5000); // Adjust the delay if necessary
    }

    // function respondToCommand(command) {
    //     // Implement the logic to respond to the voice command here
    //     showMessage();
    // }

    function showMessage() {
        const message = document.getElementById('merlin-response');
        message.innerText = 'شما می توانید به من بگویید که چه کاری می خواهید';
        message.style.display = 'block';
    }
}
