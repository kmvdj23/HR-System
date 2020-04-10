(function($) {
    "use strict"; // Start of use strict

    // Toggle the side navigation
    $("#sidebarToggle, #sidebarToggleTop").on('click', function(e) {
        $("body").toggleClass("sidebar-toggled");
        $(".sidebar").toggleClass("toggled");
        if ($(".sidebar").hasClass("toggled")) {
            $('.sidebar .collapse').collapse('hide');
        };
    });

    // Close any open menu accordions when window is resized below 768px
    $(window).resize(function() {
        if ($(window).width() < 768) {
            $('.sidebar .collapse').collapse('hide');
        };
    });

    // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
    $('body.fixed-nav .sidebar').on('mousewheel DOMMouseScroll wheel', function(e) {
        if ($(window).width() > 768) {
            var e0 = e.originalEvent,
                delta = e0.wheelDelta || -e0.detail;
            this.scrollTop += (delta < 0 ? 1 : -1) * 30;
            e.preventDefault();
        }
    });

    // Scroll to top button appear
    $(document).on('scroll', function() {
        var scrollDistance = $(this).scrollTop();
        if (scrollDistance > 100) {
            $('.scroll-to-top').fadeIn();
        } else {
            $('.scroll-to-top').fadeOut();
        }
    });

    // Smooth scrolling using jQuery easing
    $(document).on('click', 'a.scroll-to-top', function(e) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: ($($anchor.attr('href')).offset().top)
        }, 1000, 'easeInOutExpo');
        e.preventDefault();
    });

})(jQuery); // End of use strict

// Candidate Table
$('#candidate-table').DataTable({
  "pagingType": "full_numbers",
  "order": [
        // Call Count
        [8, "desc"],
        // Data Acquired
        [1, "desc"],
        // Candidate Name
        [2, "asc"]
    ]
});

// Call History Table
$('#call-history-table').DataTable({
  "pagingType": "full_numbers",
  "order": [
        // Candidate Name
        [0, "asc"]
    ]
});

// Account Records Table
$('#account-records-table').DataTable({
  "pagingType": "full_numbers",
  "order": [
        // Name
        [0, "asc"]
    ]
});

// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
var ctx = document.getElementById("chart-candidate-status");
var chartCandidateStatus = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ["Hired", "Failed", "Declined", "For Final", "For Background Check"],
        datasets: [{
            data: [55, 30, 15, 23, 10],
            backgroundColor: ['#1cc88a', '#e74a3b', '#f6c23e', '#4e73df', '#36b9cc'],
            hoverBackgroundColor: ['#17a673', '#bf4539', '#c29932', '#2e59d9', '#2c9faf'],
            hoverBorderColor: "rgba(234, 236, 244, 1)",
        }],
    },
    options: {
        maintainAspectRatio: false,
        tooltips: {
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            caretPadding: 10,
        },
        legend: {
            display: false
        },
        cutoutPercentage: 80,
    },
});

// Pie Chart Example
ctx = document.getElementById("chart-callout-status");
var chartCalloutStatus = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ["Untapped", "First Attempt", "Second Attempt", "Third Attempt"],
        datasets: [{
            data: [55, 30, 15, 5],
            backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e'],
            hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf', '#c29932'],
            hoverBorderColor: "rgba(234, 236, 244, 1)",
        }],
    },
    options: {
        maintainAspectRatio: false,
        tooltips: {
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            caretPadding: 10,
        },
        legend: {
            display: false
        },
        cutoutPercentage: 80,
    },
});

// Pie Chart Example
ctx = document.getElementById("chart-details");
var chartDetails = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ["Cannot Be Reached", "Passed", "Failed", "Executive Search", "Declined", "Phone Invite", "Specialized Recruitment", "Processed", "Active File", "Text Blast", "Wrong Number"],
        datasets: [{
            data: [6, 1, 1, 1, 2, 1, 1, 1, 1, 1],
            backgroundColor: ['#25CBB5', '#92C5BC', '#A2E6DD', '#A6DADA', '#BAF0D0', '#b581b1', '#E4DCB7', '#EAD296', '#ECCEB2', '#F4B0A7', '#F55D6A'],
            hoverBackgroundColor: ['#18A086', '#7DB6A8', '#83D4CB', '#A0C7C6', '#AEDDBB', '#7f5a7c', '#D9D3B9', '#D8BA7E', '#D9BA9C', '#DC9D8E', '#D43539'],
            hoverBorderColor: "rgba(234, 236, 244, 1)",
        }],
    },
    options: {
        maintainAspectRatio: false,
        tooltips: {
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            caretPadding: 10,
        },
        legend: {
            display: false
        },
        cutoutPercentage: 80,
    },
});

function number_format(number, decimals, dec_point, thousands_sep) {
  // *     example: number_format(1234.56, 2, ',', ' ');
  // *     return: '1 234,56'
  number = (number + '').replace(',', '').replace(' ', '');
  var n = !isFinite(+number) ? 0 : +number,
    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
    sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
    dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
    s = '',
    toFixedFix = function(n, prec) {
        var k = Math.pow(10, prec);
        return '' + Math.round(n * k) / k;
    };
  // Fix for IE parseFloat(0.55).toFixed(0) = 0;
  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || '').length < prec) {
    s[1] = s[1] || '';
    s[1] += new Array(prec - s[1].length + 1).join('0');
  }
  return s.join(dec);
}

// Bar Chart Example
ctx = document.getElementById("chart-hr-process");
var chartHRProcess = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ["John Doe", "Jane Eyre", "Robert Brown"],
    datasets: [{
        label: "Applications Processed",
        backgroundColor: "#4e73df",
        hoverBackgroundColor: "#2e59d9",
        borderColor: "#4e73df",
        data: [10, 14, 25],
    }],
  },
  options: {
    maintainAspectRatio: false,
    layout: {
        padding: {
            left: 10,
            right: 25,
            top: 25,
            bottom: 0
        }
    },
    scales: {
      xAxes: [{
        time: {
            unit: 'month'
        },
        gridLines: {
            display: false,
            drawBorder: false
        },
        ticks: {
            maxTicksLimit: 6
        },
        maxBarThickness: 25,
      }],
      yAxes: [{
        ticks: {
            min: 0,
            max: 50,
            maxTicksLimit: 10,
            padding: 10,
            callback: function(value, index, values) {
                return number_format(value);
            }
        },
        gridLines: {
            color: "rgb(234, 236, 244)",
            zeroLineColor: "rgb(234, 236, 244)",
            drawBorder: false,
            borderDash: [2],
            zeroLineBorderDash: [2]
        }
      }],
    },
    legend: {
        display: false
    },
    tooltips: {
        titleMarginBottom: 10,
        titleFontColor: '#6e707e',
        titleFontSize: 14,
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        caretPadding: 10,
        callbacks: {
            label: function(tooltipItem, chart) {
                var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
                return datasetLabel + ': ' + number_format(tooltipItem.yLabel);
            }
        }
    },
  }
});
