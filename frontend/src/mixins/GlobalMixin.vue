<script>
export default {
  name: "GlobalMixin",

  methods: {
    GetCurrentUser: function() {
      return window.localStorage.getItem("username");
    },
    showNotify: function(text, color) {
      this.$toast(text, {
        x: "left",
        y: "bottom",
        color: color,
        icon: "mdi-information",
        iconColor: "",
        classes: ["body-2"],
        timeout: 3000,
        dismissable: true,
        multiLine: true,
        vertical: false,
        queueable: true,
        showClose: true,
        closeText: "",
        closeIcon: "mdi-close",
        closeColor: "",
        slot: [],
        shorts: {
          custom: {
            color: "purple"
          }
        },
        property: "$toast"
      });
    },
  }
};
</script>
