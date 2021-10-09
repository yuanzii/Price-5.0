<template>
  <v-app>
    <router-view></router-view>
  </v-app>
</template>


<script>
export default {
  name: "product_category",
  data() {
    return {};
  },
  created: function () {
    this.level_1_auto();
  },
  computed: {},
  methods: {
    level_1_auto() {
      console.log("level_1_auto");
      this.$router.push({
        path: "/product_category/level_1",
      });
    },
  },
};
</script>