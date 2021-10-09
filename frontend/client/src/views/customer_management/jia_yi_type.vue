<template>
  <v-app>
    <v-container fluid style="margin-top: 30px">
      <v-row>
        <!--Page 1-->
        <v-col cols="3">
          <div id="page1">
            <!--Add Customer Type To Sql-->
            <v-card outlined style="height: 350px">
              <v-card-title style="margin-top: 10px">
                <span class="headline">Add Customer Type</span>
              </v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <span class="headline">Level-1</span>
                <!--Product Category Form-->
                <v-form lazy-validation ref="category_form">
                  <v-row
                    ><v-col cols="12" style="margin-top: 15px">
                      <v-text-field
                        v-model="jia_yi_type.name"
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
            <!--Type List-->
            <v-card outlined>
              <v-card-title style="margin-top: 10px; margin-bottom: -20px">
                <span class="headline">Type List</span></v-card-title
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

              <v-data-table
                :headers="headers"
                :items="jia_yi_type_list"
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
  </v-app>
</template>


<script>
import axios from "axios";
export default {
  name: "about",
  data() {
    return {
      valid: true,

      jia_yi_type: {
        id: "",
        name: "",
        c_id: "",
        level: "",
      },

      rules: [(v) => !!v || "ကွက်လပ်မထားရပါ။"],

      search: "",
      jia_yi_type_list: [],

      //   Edit Dialog
      edit_dialog: false,
      edit_list: "",
    };
  },
  created: function () {
    this.load_data();
  },
  computed: {
    headers() {
      return [
        { text: "ID", align: "start", value: "id" },
        { text: "အမျိုးအမည်", value: "name" },
        { text: "အမျိုးအမည်ID", value: "c_id" },
        { text: "အဆင့် Level", value: "level" },
        { text: "View", value: "next_level" },
      ];
    },
  },
  methods: {

    load_data() {
      var send_info = {
        level: 1,
        id: 0,
      };
      const path = this.$api + "/jia_yi_type_api_v1";
      axios
        .post(path, send_info)
        .then((res) => {
          this.jia_yi_type_list = [res.data][0];
        })
        .catch((error) => {
          console.error(error);
        });
    },

	// ADD/UPDATE : Insert To sql
    level_1() {
      console.log("add level_1");
      const valid = this.$refs.category_form.validate();
      if (valid === true) {
        var send_info = {
          name: this.jia_yi_type.name,
          c_id: 0, //c_id
          level: 1,
        };
        console.log(send_info);
        const path = this.$api + "/jia_yi_type_api_v1";
        axios
          .post(path, send_info)
          .then((res) => {
            //   this.jia_yi_type.name = res.data.mm_name;
            console.log(res.data);
            this.load_data();
          })
          .catch((error) => {
            console.error(error);
          });
        this.$refs.category_form.reset();
      } else {
        console.log("ERROR");
      }
    },

	//   EDIT
    edit_dialog_(item) {
      this.edit_list = {
        id: item.id,
        name: item.name,
        c_id: item.c_id,
        level: item.level,
      };
      this.edit_dialog = true;
    },
    updated() {
      var send_info = this.edit_list;
      console.log(send_info);
      const path = this.$api + "/jia_yi_type_api_v1";
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

    level_2(item) {
      console.log(item);
      //   console.log(item.id);
      //   this.$router.push({
      //     path: "/product_category/level_2/",
      //     query: {
      //       id: item.id,
      //     },
      //   });
    },
  },
};
</script>