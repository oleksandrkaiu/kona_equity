$("#companies").change(function () {
  var selectedValue = $(this).val();

  switch (selectedValue) {
    case "software company":
      $('#companies_number').text("100,000+ companies tracked");
      break;
    case "manufacturer":
      $('#companies_number').text("80,000+ companies tracked");
      break;
    case "insurance agency":
      $('#companies_number').text("70,000+ companies tracked");
      break;
    case "financial company":
      $('#companies_number').text("45,000+ companies tracked");
      break;
    case "consultant":
      $('#companies_number').text("100,000+ companies tracked");
      break;
    case "pharmaceutical company":
      $('#companies_number').text("5,000+ companies tracked");
      break;
    case "biotech company":
      $('#companies_number').text("20,000+ companies tracked");
      break;
    case "telecommunications provider":
      $('#companies_number').text("10,000+ companies tracked");
      break;
    case "food":
      $('#companies_number').text("80,000+ companies tracked");
      break;
    case "Select category":
      $('#companies_number').text("2.5 million+ companies tracked");
      break;
    default:
      $('#companies_number').text("2.5 million+ companies tracked");
      break;
  }
});
