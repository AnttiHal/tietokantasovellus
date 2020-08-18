var counter=0;
        function play() {
            if(counter<4) {
                var audio = document.getElementById('chord');
                    if (audio.paused) {
                    audio.play();
                    counter++;
            }else{
                audio.currentTime = 0
                counter++;
            }
            }
            else{
            document.getElementById("chord").disabled=true;
            }
        }