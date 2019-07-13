// require("persian-date");
import "bootstrap";
import "persian-datepicker/dist/js/persian-datepicker";


import "bootstrap-v4-rtl/dist/css/bootstrap-rtl.css";
import "persian-datepicker/dist/css/persian-datepicker.css";
import "@fortawesome/fontawesome-free/css/all.css";
// import "@fortawesome/fontawesome-free/webfonts";
import "../css/fonts.css";
import "../css/general.css";
import "../css/login.css";

$("document").ready(function() {
  $(".datepicker").pDatepicker({
    initialValueType: "persian",
    initialValue: false,
    format: "YYYY-M-D"
  });

  $("#btnFetchTitle").click(function() {
    if ($("#id_url").val()) {
      $.ajax({
        type: "GET",
        url: "fetch_title",
        data: {
          url: $("#id_url").val()
        }
      })
        .done(function(data) {
          if (data.title) {
            $("#id_title").val(data.title);
          }
          if (data.error) {
            console.log(data.error);
          }
        })
        .fail(function(jqXHR, textStatus) {
          console.log(textStatus);
        });
    }
  });

});
