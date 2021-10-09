<template>
  <v-app id="inspire">
    <!-- <v-card height="350px"> -->
    <v-navigation-drawer absolute permanent left>
      <template v-slot:prepend>
        <v-list-item two-line>
          <v-list-item-avatar>
            <img src="https://randomuser.me/api/portraits/women/81.jpg" />
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title>Jane Smith</v-list-item-title>
            <v-list-item-subtitle>Logged In</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </template>

      <v-divider></v-divider>

      <v-list dense>
        <v-list-item
          v-for="item in items"
          :key="item.title"
          :to="item.path"
          link
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title v-text="item.title"></v-list-item-title>
            <!-- {{ item.title }} -->
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <!-- </v-card> -->

    <router-view style="margin-left: 250px"></router-view>
  </v-app>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      items: [
        { title: "Home", path: "/", icon: "home" },
        { title: "Product Category",path: "/product_category",icon: "grid_view"},
		{ title: "Price Parameter",path: "/kt_price_parameter",icon: "grid_view"},
		// { title: "Price Parameter",path: "/duty",icon: "grid_view"},
        { title: "Product InFo", path: "/product_info", icon: "local_parking" },
        { title: "Customer Type Category", path: "/jia_yi_type", icon: "grid_view" },
        { title: "Customer InFo", path: "/jia_yi_info", icon: "person" },
      ],
    };
  },
};
</script>