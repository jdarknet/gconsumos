(function() {
    var CalendarEvent, CalendarEvents, ConfirmAction,
        __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

    CalendarEvent = (function() {

        function CalendarEvent(container, add) {
            var input;
            this.container = container;
            this.makeFullCalendarEventObject = __bind(this.makeFullCalendarEventObject, this);

            this.handleDoubleClick = __bind(this.handleDoubleClick, this);

            this.finalizeEvent = __bind(this.finalizeEvent, this);

            this.handleInputBlur = __bind(this.handleInputBlur, this);

            this.handleInputKeyup = __bind(this.handleInputKeyup, this);

            this.container.bind("dblclick", this.handleDoubleClick);
            if (add != null) {
                input = this.container.find("input");
                input.focus();
                input.bind("keyup", this.handleInputKeyup);
                input.bind("blur", this.handleInputBlur);
            } else {
                this.makeFullCalendarEventObject();
            }
        }

        CalendarEvent.prototype.handleInputKeyup = function(e) {
            var input;
            input = $(e.target);
            if (e.keyCode === 13) {
                if (input.val().length === 0) {
                    return this.container.remove();
                } else {
                    return this.finalizeEvent(input.val());
                }
            }
        };

        CalendarEvent.prototype.handleInputBlur = function(e) {
            var input;
            input = $(e.target);
            if (input.val().length === 0) {
                return this.container.remove();
            } else {
                return this.finalizeEvent(input.val());
            }
        };

        CalendarEvent.prototype.finalizeEvent = function(val) {
            this.container.find("a").html(val);
            return this.makeFullCalendarEventObject();
        };

        CalendarEvent.prototype.handleDoubleClick = function(e) {
            var input, link, oldval,
                _this = this;
            input = $("<input type='text'>");
            link = $(e.target);
            oldval = link.text();
            input.val(oldval);
            link.html(input);
            input.focus();
            input.bind("keyup", function(e) {
                if (e.keyCode === 13) {
                    if (input.val().length > 0) {
                        link.html(input.val());
                        return _this.makeFullCalendarEventObject();
                    } else {
                        return link.html(oldval);
                    }
                }
            });
            return input.bind("blur", function(e) {
                if (input.val().length > 0) {
                    link.html(input.val());
                    return _this.makeFullCalendarEventObject();
                } else {
                    return link.html(oldval);
                }
            });
        };

        CalendarEvent.prototype.makeFullCalendarEventObject = function() {
            var eventObject, link;
            link = $(this.container);
            eventObject = {
                title: $.trim(link.text())
            };
            link.data('eventObject', eventObject);
            return link.draggable({
                zIndex: 999,
                revert: true,
                revertDuration: 0
            });
        };

        return CalendarEvent;

    })();

    CalendarEvents = (function() {

        function CalendarEvents(container) {
            this.container = container;
            this.handleAddLink = __bind(this.handleAddLink, this);

            this.addLink = this.container.find("#add-event");
            this.container.find("a.external-event").each(function() {
                return new CalendarEvent($(this));
            });
            this.template = "<li><a class='external-event'><input type='text'></a></li>";
            this.addLink.bind("click", this.handleAddLink);
        }

        CalendarEvents.prototype.handleAddLink = function() {
            var view;
            view = $(this.template);
            view.insertBefore(this.addLink.parent());
            return new CalendarEvent(view, true);
        };

        return CalendarEvents;

    })();


    $(function() {
        $("html, body").off("touchstart");
        var opts = {
            lines: 13, // The number of lines to draw
            length: 7, // The length of each line
            width: 4, // The line thickness
            radius: 26, // The radius of the inner circle
            corners: 1, // Corner roundness (0..1)
            rotate: 0, // The rotation offset
            color: '#000', // #rgb or #rrggbb
            speed: 1, // Rounds per second
            trail: 60, // Afterglow percentage
            shadow: false, // Whether to render a shadow
            hwaccel: false, // Whether to use hardware acceleration
            className: 'spinner', // The CSS class to assign to the spinner
            zIndex: 2e9, // The z-index (defaults to 2000000000)
            top: 'auto', // Top position relative to parent in px
            left: 'auto' // Left position relative to parent in px
        };

        $.fn.spin = function(opts, color) {
            var presets = {
                "tiny": { lines: 8, length: 2, width: 2, radius: 3 },
                "small": { lines: 8, length: 4, width: 3, radius: 5 },
                "large": { lines: 10, length: 8, width: 4, radius: 8 }
            };
            if (Spinner) {
                return this.each(function() {
                    var $this = $(this),
                        data = $this.data();

                    if (data.spinner) {
                        data.spinner.stop();
                        delete data.spinner;
                    }
                    if (opts !== false) {
                        if (typeof opts === "string") {
                            if (opts in presets) {
                                opts = presets[opts];
                            }
                            else {
                                opts = {};
                            }
                            if (color) {
                                opts.color = color;
                            }
                        }
                        data.spinner = new Spinner($.extend({color: $this.css('color')}, opts)).spin(this);
                    }
                });
            }
            else
            {
                throw "Spinner class not available.";
            }
        };



        $("#modal-link").click(function() {
            return $('#modal').modal();
        });
        $('.input-error').tooltip();
        $(".chzn-select").chosen();
        $('textarea.tagme').tagify();
        new Faq($(".faq-list"));
        new CalendarEvents($('#external-events'));
        $('.data-table').dataTable({
            "bJQueryUI": true,
            "sPaginationType": "full_numbers",
            "sDom": '<""l>t<"F"fp>'
        });
        return $("#calendar").fullCalendar({
            header: {
                left: 'prev,next today',
                center: 'title',
                right: 'month,agendaWeek,agendaDay'
            },
            editable: true,
            droppable: true,
            drop: function(date, allDay) {
                var copiedEventObject, originalEventObject;
                originalEventObject = $(this).data('eventObject');
                copiedEventObject = $.extend({}, originalEventObject);
                copiedEventObject.start = date;
                copiedEventObject.allDay = allDay;
                $("#calendar").fullCalendar('renderEvent', copiedEventObject, true);
                if ($("#drop-remove").is(":checked")) {
                    return $(this).remove();
                }
            }
        });
    });

}).call(this);

