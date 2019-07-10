// require("persian-date");
import "bootstrap";
import "persian-datepicker/dist/js/persian-datepicker";


import "bootstrap-v4-rtl/dist/css/bootstrap-rtl.css";
import "persian-datepicker/dist/css/persian-datepicker.css";
// import "@fortawesome/fontawesome-free/webfonts";
import "../css/fonts.css";
import "../css/general.css";

$("document").ready(function() {
  $(".datepicker").pDatepicker({
    initialValueType: "persian",
    initialValue: false,
    format: "YYYY-M-D"
  });
});
