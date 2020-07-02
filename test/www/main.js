fetch('/user.cgi').then(function (response) {
  response.json().then(function (data) {
    console.log(data);
  });
});
