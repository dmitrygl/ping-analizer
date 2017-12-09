var xhr = new XMLHttpRequest();
xhr.open("POST", "http://pinganalizer/scripts/ping_analizer.py", true);
xhr.send();
xhr.onreadystatechange = function() {
        if (xhr.readyState == 4){
                var data = xhr.responseText;
                var red = -1;
                var green = -1;
                var orange = -1;
                var countR = 0;
                var countG = 0;
                var countO = 0;
                while ((red = data.indexOf('red', red + 1)) != -1) {
                        countR += 1;
                        document.getElementById('blockR').innerHTML = countR;
                }
                while ((green = data.indexOf('green', green + 1)) != -1){
                        countG += 1;
                        document.getElementById('blockG').innerHTML = countG;
                }
                while ((orange = data.indexOf('orange', orange + 1)) != -1){
                        countO += 1;
                        document.getElementById('blockO').innerHTML = countO;
                }
        }
};


