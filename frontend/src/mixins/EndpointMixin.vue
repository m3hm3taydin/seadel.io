<script>
import { CSRF_TOKEN } from "@/common/csrf_token.js";

export default {
  name: "EndpointMixin",
  methods: {
    // User
    GetUserInfoMixin(completed) {
      let endpoint = "/api/user/";
      this.GetData(endpoint, completed);
    },

    GetData(endpoint, completed) {
      let headers = {
        "content-type": "application/json",
        "X-CSRFTOKEN": CSRF_TOKEN
      };

      let _self = this;

      this.axios
        .get(endpoint, {
          headers: headers
        })
        .then(function(data) {
          if (data.status == 200) {
            completed(data.data);
          } else {
            if (data.Message == "NotAuthorized") {
              // swal.closeModal();
              _self.showNotify("Not Authorised", "red");

              // GlobalHelper.showNotify(false, lang('BrowserView.notAuthotized.text') + (data.IdentityName ? (': ' + data.IdentityName) : ''), 'error');
              completed();
            } else {
              // console.error(data.Message);
              _self.showNotify("Error :\n" + data, "red");

              console.log("Response: ", data);
              completed();
            }
          }
        })
        .catch(function(error) {
          _self.showNotify("Error : " + error.status + "\n" + error, "red");

          console.error(error.status + " " + error.statusText);
          console.log("Response: ", error);
          completed();
        });
    }
  }
};
</script>
