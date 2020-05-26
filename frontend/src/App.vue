<template>
  <v-app>
    <v-app-bar
      color="#fcb69f"
      dark
      src="https://i.picsum.photos/id/654/1920/1080.jpg"
      app
    >
      <!-- src="https://picsum.photos/1920/1080?random" -->

      <template v-slot:img="{ props }">
        <v-img
          v-bind="props"
          gradient="to top right, rgba(19,84,122,.5), rgba(128,208,199,.8)"
        ></v-img>
      </template>

      <v-app-bar-nav-icon></v-app-bar-nav-icon>

      <!-- <v-toolbar-title>Home</v-toolbar-title> -->

      <v-btn text href="/">
        seadel.io
      </v-btn>


      <v-spacer></v-spacer>

      <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>

      <v-btn icon>
        <v-icon>mdi-heart</v-icon>
      </v-btn>

      <v-btn icon>
        <v-icon>mdi-dots-vertical</v-icon>
      </v-btn>

      <v-btn text>
        {{ requestUser }}
      </v-btn>
    </v-app-bar>

    <!-- Sizes your content based upon application components -->
    <v-content>
      <!-- Provides the application the proper gutter -->
      <v-container fluid>
        <!-- If using vue-router -->
        <router-view></router-view>
      </v-container>
    </v-content>

    <v-footer dark padless app>
      <v-card class="flex" flat tile>
        <v-card-text class="py-0 white--text">
          <v-row>
            <v-col> </v-col>
            <v-col class="text-center">
              {{ new Date().getFullYear() }} — <strong>seadel.io</strong>
              <!-- <v-spacer></v-spacer> -->
            </v-col>
            <v-col class="text-right">
              <v-btn v-for="icon in icons" :key="icon" class="mx-1" dark icon>
                <v-icon size="24px">{{ icon }}</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: "App",
  components: {},
  data() {
    return {
      types: [],
      requestUser: null,
      icons: ["mdi-facebook", "mdi-twitter", "mdi-linkedin", "mdi-instagram"]
    };
  },
  methods: {
    setUserInfo() {
      this.GetUserInfoMixin(data => {
        const requestUser = data["username"];
        window.localStorage.setItem("username", requestUser);
      });
    },
    setRequestUser() {
      this.requestUser = this.GetCurrentUser();
    }
  },
  created() {
    this.setUserInfo();
    this.setRequestUser();
    document.title = "Seadel App";
  }
};
</script>
