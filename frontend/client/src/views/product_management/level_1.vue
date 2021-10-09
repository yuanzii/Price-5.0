<template>
  <v-app>
    <v-container fluid style="margin-top: 30px">
      <v-row>
        <!--Page 1-->
        <v-col cols="3">
          <div id="page1">
            <!--Add Product Category To Sql-->
            <v-card outlined style="height: 350px">
              <v-card-title style="margin-top: 10px">
                <span class="headline">Add Product Category</span>
              </v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <span class="headline">Level-1</span>
                <!--Product Category Form-->
                <v-form v-model="valid" ref="category_form">
                  <v-row
                    ><v-col cols="12" style="margin-top: 15px">
                      <v-text-field
                        v-model="product_category.name"
                        :rules="rules"
                        label=" "
                        @keyup.enter="level_1"
                        outlined
                        autofocus
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <!--Add To Sql Btn-->
                  <v-row>
                    <v-col
                      class="pt-0"
                      style="margin-top: -10px; margin-bottom: 15px"
                    >
                      <v-btn
                        rounded
                        large
                        block
                        :disabled="!valid"
                        color="blue-grey lighten-2"
                        @click="level_1"
                      >
                        Add
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-form>
              </v-card-text>
            </v-card>
          </div>
        </v-col>

        <!--Page 2-->
        <v-col cols="9">
          <div id="page2">
            <!--Category List-->
            <v-card outlined>
              <v-card-title style="margin-top: 10px; margin-bottom: -20px">
                <span class="headline">Category List</span></v-card-title
              >

              <!-- Edit Dialog -->
              <v-dialog v-model="edit_dialog" persistent max-width="290">
                <v-card>
                  <v-card-title class="headline">
                    <!-- Edit Name -->
                  </v-card-title>
                  <v-card-text
                    ><v-row
                      ><v-col cols="12" style="margin-top: 15px">
                        <v-text-field
                          v-model="edit_list.name"
                          :rules="rules"
                          label=" "
                          @keyup.enter="level_1"
                          outlined
                          autofocus
                        ></v-text-field>
                      </v-col> </v-row
                  ></v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                      color="black darken-1"
                      text
                      @click="edit_dialog = false"
                    >
                      ပယ်ဖျက်
                    </v-btn>
                    <v-btn color="green darken-1" text @click="updated()">
                      အတည်ပြု
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>

              <!-- Delete Dialog -->
              <v-dialog v-model="delete_dialog" persistent max-width="290">
                <v-card>
                  <v-card-title class="headline"></v-card-title>
                  <v-card-text>ဖျက်မှုကိုအတည်ပြုပါသလား?</v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                      color="black darken-1"
                      text
                      @click="delete_dialog = false"
                    >
                      ပယ်ဖျက်
                    </v-btn>
                    <v-btn color="red darken-1" text @click="deleted()">
                      အတည်ပြု
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>

              <!-- Warm Dialog -->
              <v-dialog v-model="warm_dialog" persistent max-width="290">
                <v-card>
                  <v-card-title class="headline"></v-card-title>
                  <v-card-text
                    >ဖျက်လို့မရ။ နောက်တစ်မျက်နှာသို့သွားပါ။</v-card-text
                  >
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                      color="black darken-1"
                      text
                      @click="warm_dialog = false"
                    >
                      OK
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>

              <v-data-table
                :headers="headers"
                :items="product_category_list"
                item-key="idname"
                class="elevation-1"
                style="margin-top: 30px"
              >
                <template v-slot:item.next_level="{ item }">
                  <!-- Btn -->
                  <v-btn
                    style="cursor: move"
                    icon
                    class="sortHandle"
                    @click="edit_dialog_(item)"
                  >
                    <v-icon>edit</v-icon>
                  </v-btn>
                  <v-btn
                    style="cursor: move"
                    icon
                    class="sortHandle"
                    @click="delete_dialog_(item)"
                  >
                    <v-icon>delete</v-icon>
                  </v-btn>
                  <v-btn
                    style="cursor: move"
                    icon
                    class="sortHandle"
                    @click="level_2(item)"
                  >
                    <v-icon>control_point</v-icon>
                  </v-btn>
                </template>
              </v-data-table>
            </v-card>
          </div>
        </v-col>
      </v-row>
    </v-container>
    <pre>delete_list:{{ delete_list }}</pre>
  </v-app>
</template>


<script>
import axios from "axios";
export default {
  name: "about",
  data() {
    return {
      valid: false,
      product_category: {
        id: "",
        name: "",
        c_id: "",
        level: "",
      },
      rules: [(v) => !!v || "ကွက်လပ်မထားရပါ။"],
      search: "",
      product_category_list: [],

      //   Edit Dialog
      edit_dialog: false,
      edit_list: "",

      //   Delete Dialog
      delete_dialog: false,
      delete_list: "",

      warm_dialog: false,
    };
  },
  created: function () {
    this.load_data();
  },
  computed: {
    headers() {
      return [
        { text: "ID", align: "start", value: "id_x" },
        { text: "အမျိုးအမည်", value: "name_x" },
        { text: "အုပ်စုအမည်", value: "name_y" },
        { text: "အဆင့် Level", value: "level_x" },
        { text: "View", value: "next_level" },
      ];
    },
  },
  methods: {
    //   LOAD DATA
    load_data() {
      var send_info = {
        level: 1,
        id: 0,
      };
      const path = this.$api + "/product_category_api";
      axios
        .post(path, send_info)
        .then((res) => {
          //   console.log([res.data][0]);
          this.product_category_list = [res.data][0];
          console.log(this.product_category_list);
        })
        .catch((error) => {
          console.log("Empty Data");
          console.log(error);
        });
    },

    // ADD/UPDATE : Insert To sql
    level_1() {
      console.log("add level_1");
      var send_info = {
        name: this.product_category.name,
        c_id: 0, //c_id
        level: 1,
      };
      console.log(send_info);
      const path = this.$api + "/product_category_api";
      axios
        .post(path, send_info)
        .then((res) => {
          //   this.product_category.name = res.data.mm_name;
          console.log(res.data);
          this.load_data();
        })
        .catch((error) => {
          console.error(error);
        });
      this.$refs.category_form.reset();
    },

    //   EDIT
    edit_dialog_(item) {
      this.edit_list = {
        id: item.id_x,
        name: item.name_x,
        c_id: item.name_y,
        level: item.level_x,
      };
      this.edit_dialog = true;
    },
    updated() {
      var send_info = this.edit_list;
      console.log(send_info);
      const path = this.$api + "/product_category_api";
      axios
        .put(path, send_info)
        .then((res) => {
          console.log(res);
          this.load_data();
        })
        .catch((error) => {
          console.error(error);
        });
      this.edit_dialog = false;
    },

    // DELETE
    delete_dialog_(item) {
      var send_info = {
        variable: 0,
        id: item.id_x,
        name: item.name_x,
        c_id: item.name_y,
        level: item.level_x,
      };
      const path = this.$api + "/product_category_api";
      axios
        .put(path, send_info)
        .then((res) => {
          console.log(res.data);
          if (res.data.length == 0) {
            this.delete_list = item;
            this.delete_dialog = true;
          } else {
            this.warm_dialog = true;
            console.log("有東西");
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    deleted() {
      var send_info = {
        variable: 1,
        id: this.delete_list.id_x,
        name: this.delete_list.name_x,
        c_id: this.delete_list.name_y,
        level: this.delete_list.level_x,
      };
      console.log(send_info);
      const path = this.$api + "/product_category_api";
      axios
        .put(path, send_info)
        .then((res) => {
          console.log(res);
          this.load_data();
        })
        .catch((error) => {
          console.error(error);
        });
      this.delete_dialog = false;
    },

    // View Next Level
    level_2(item) {
      console.log(item);
      //   console.log(item.id_x);
      this.$router.push({
        path: "/product_category/level_2/",
        query: {
          id: item.id_x,
		  level: item.level_x,
        },
      });
    },
  },
};
</script>