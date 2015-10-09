var deployed = false;
var full_months = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"]
var days = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]

function toggle(elmt){
    if(elmt.style.display == "none"){
        elmt.style.display = "block";
    }
    else{
        elmt.style.display = "none";
    }
}

function addEvent(obj, event_type, callback){
    if(obj.attachEvent){
        obj.attachEvent("on" + event_type, callback)
    }
    else{
        obj.addEventListener(event_type, callback);
    }
}

function debounce(method, delay){
    clearTimeout(method._tId);
    method._tId = setTimeout(function(){
        method();
    }, delay);
}

function create_calendar(id){
    var input = document.getElementById(id);
    var date = input.value;
    var parsed_date = date.split('/');
    if(date){
        var year = parsed_date[2];
        var month = parsed_date[1] - 1;
        var day = parsed_date[0];
    }
    else{
        var d = new Date()
        var year = d.getFullYear();
        var month = d.getMonth();
        var day = d.getDate();
    }
    var current_date = new Date(year, month, 1, 1, 0, 0);

    var contentDiv = document.createElement("div");
    var titleBar = document.createElement("div");
    var nextButton = document.createElement("a");
    var prevButton = document.createElement("a");
    var monthSpan = document.createElement("span");
    var yearInput = document.createElement("input");
    var calendarDiv = document.createElement("div");


    contentDiv.id = id;
    contentDiv.className = "cal";
    contentDiv.style.display = "none";

    titleBar.className = "cal_title";
    yearInput.type = "text";
    yearInput.value = year;

    prevButton.innerHTML = "<i class='fa fa-chevron-left'></i> ";
    prevButton.href = "#";
    monthSpan.innerHTML = full_months[month];
    nextButton.href = "#";
    nextButton.innerHTML = "<i class='fa fa-chevron-right'></i>";

    titleBar.appendChild(prevButton);
    titleBar.appendChild(monthSpan);
    titleBar.appendChild(yearInput);
    titleBar.appendChild(nextButton);
    contentDiv.appendChild(titleBar);
    contentDiv.appendChild(calendarDiv);

    input.parentNode.insertBefore(contentDiv, input.nextSibling);

    addEvent(prevButton, "click", function(){
        current_date.setMonth(current_date.getMonth() - 1);
        year = current_date.getFullYear();
        month = current_date.getMonth();
        yearInput.value = year;
        monthSpan.innerHTML = full_months[month];
        refresh(calendarDiv, current_date, input);
    });

    addEvent(nextButton, "click", function(){
        current_date.setMonth(current_date.getMonth() + 1);
        year = current_date.getFullYear();
        month = current_date.getMonth();
        yearInput.value = year;
        monthSpan.innerHTML = full_months[month];

        refresh(calendarDiv, current_date, input);
    });

    addEvent(input, "click", function(){
        monthSpan.innerHTML = full_months[month];
        refresh(calendarDiv, current_date, input);
        toggle(contentDiv);
    });

    addEvent(document.getElementsByTagName("html")[0], "click", function(event){
        if(event.srcElement){
            if(event.srcElement != input){
                contentDiv.style.display = "none";
            }
        }
        else{
            if(event.target != input){
                contentDiv.style.display = "none";
            }
        }
    });

    addEvent(contentDiv, "click", function(event){
        if(event.stopPropagation){
            event.stopPropagation();
            event.preventDefault();
        }
        else{
            window.event.returnValue = false;
            window.event.cancelBubble = true;
        }
    });

    addEvent(yearInput, "keypress", function(event){
        if(event.keyCode != 13){
            return;
        }
        if(event.srcElement){
            current_date.setYear(event.srcElement.value);
        }
        else{
            current_date.setYear(event.target.value);
        }
        refresh(calendarDiv, current_date, input);

        // Does not work
        if(event.stopPropagation){
            event.stopPropagation();
            event.preventDefault();
        }
        else{
            window.event.returnValue = false;
            window.event.cancelBubble = true;
        }
    });

    addEvent(window, 'resize', function(event){
        replace_cal(input, contentDiv)
    });
    addEvent(window, 'scroll', function(event){
        debounce(replace_cal.bind(null, input, contentDiv), 10)
    });

    refresh(calendarDiv, current_date, input);
    debounce(replace_cal.bind(null, input, contentDiv), 10)
}

function replace_cal(input, contentDiv){
    pos = input.getBoundingClientRect();
    scroll = document.body.scrollTop
    var height = window.innerHeight;
    contentDiv.style.left = pos.x + scroll + 'px';
    contentDiv.style.top = Math.min(pos.y, height-266) + 'px';
}

function refresh(cal_div, first_day, input){
    var last_day = new Date(first_day.getFullYear(), first_day.getMonth() + 1, 0);
    var table = document.createElement("table");
    var tr = document.createElement("tr")
    var can_be_hl = false;

    for(var d in days){
        var th = document.createElement("th");
        th.innerHTML = days[d];
        tr.appendChild(th);
    }
    if(input.value){
        date = input.value.split('/');
        day = date[0];
        month = date[1];
        year = date[2];
        if((parseInt(first_day.getMonth()) + 1)== month && first_day.getFullYear() == year){
            can_be_hl = true;
        }
    }
    table.appendChild(tr);
    var lines = Math.ceil((last_day.getDate() + ((first_day.getDay()-1 == -1)?6:first_day.getDay() -1)) / 7);
    for(var i=0; i < lines; i++){
        line = document.createElement("tr");
        for(var j=0; j < 7; j++){
            var td = document.createElement("td");

            var u = first_day.getDay() - 1
            if(u == -1){
                u = 6;
            }
            if((i != 0 || j + 1 > first_day.getDay() -1) && (i*7 +j - u) < last_day.getDate() && (i*7+j+1-u) > 0){
                td.innerHTML = (i*7 + j + 1) -  u;
                if(can_be_hl && parseInt(td.innerHTML) == day){
                    td.setAttribute('class', 'selected');
                }
                addEvent(td, "click", function(event){
                    if(event.srcElement){
                        this_ = event.srcElement;
                    }
                    else{
                        this_ = event.target
                    }
                    input.value = ('0' + this_.innerHTML).slice(-2) + '/' + ('0' + (parseInt(first_day.getMonth())+1)).slice(-2) + '/' + first_day.getFullYear();
                    this_.parentNode.parentNode.parentNode.parentNode.parentNode.style.display = "none";
                    if ("createEvent" in document) {
                        var evt = document.createEvent("HTMLEvents");
                        evt.initEvent("change", false, true);
                        input.dispatchEvent(evt);
                    }
                    else{
                        input.fireEvent("onchange");
                    }
                });
            }
            line.appendChild(td);
        }
        table.appendChild(line);
    }
    if(cal_div.firstChild){
        cal_div.removeChild(cal_div.firstChild);
    }
    div = document.createElement("div");
    div.appendChild(table);
    cal_div.appendChild(div);
}

