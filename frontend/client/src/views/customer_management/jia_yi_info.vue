<template>
  <v-app>
    <v-container fluid style="margin-top: 15px">
      <v-row>
        <!--Page 1-->
        <v-col cols="4">
          <div id="page1">
            <!--Add Jia Yi Category To Sql-->
            <v-card outlined>
              <v-card-title style="margin-top: 10px">
                <span class="headline">Jia Yi Category</span>
              </v-card-title>
              <v-card-text>
                <!--Jia Yi Form-->
                <v-form lazy-validation ref="category_form" v-model="valid">
                  <v-row
                    ><v-col cols="12">
                      <v-text-field
                        v-model="jia_yi_name.jia_yi_idname"
                        :rules="rules"
                        label="ကုဒ်နံပါတ်"
                        @keyup.enter="enter_jia_yi_mm_name"
                        @keyup.delete="delete_customer_id"
                        outlined
                        autofocus
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row
                    ><v-col cols="12" style="margin-top: -20px">
                      <v-text-field
                        v-model="jia_yi_name.jia_yi_mm_name"
                        :rules="rules"
                        label="နာမည်"
                        outlined
                        readonly
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <!-- Level-1 -->
                  <!-- <v-row>
                    <v-col cols="12" style="margin-top: -20px">
                      <v-select
                        v-model="select_level_1"
                        :items="level_1"
                        :rules="rules"
                        item-text="name"
                        label="ပြည်နယ်"
                        @click="add_level_1"
                        return-object
                        outlined
                      ></v-select>
                    </v-col>
                  </v-row> -->
                  <!-- Level-2 -->
                  <!-- <v-row>
                    <v-col cols="12" style="margin-top: -20px">
                      <v-select
                        v-model="select_level_2"
                        :items="level_2"
                        :rules="rules"
                        item-text="name"
                        label="ခရိုင်"
                        return-object
                        outlined
                      ></v-select>
                    </v-col>
                  </v-row>
                  <v-row> -->
                  <!-- Level-3 -->
                  <!-- <v-col cols="12" sm="6" style="margin-top: -20px">
                      <v-select
                        v-model="select_level_3"
                        :items="level_3"
                        :rules="rules"
                        item-text="name"
                        label="မြို့နယ်/မြို့နယ်ခွဲ"
                        return-object
                        outlined
                      ></v-select>
                    </v-col> -->
                  <!-- Level-4 -->
                  <!-- <v-col cols="12" sm="6" style="margin-top: -20px">
                      <v-select
                        :items="level_4"
                        item-text="name"
                        label="ရပ်ကွက်/ကျေးရွာအုပ်စု"
                        return-object
                        outlined
                      ></v-select>
                    </v-col>
                  </v-row> -->
                  <!-- Jia Yi Type -->
                  <v-row>
                    <v-col cols="12" style="margin-top: -20px">
                      <v-select
                        v-model="select_shop"
                        :items="shop_category"
                        :rules="rules"
                        item-text="name"
                        label="ဆိုင်"
                        @click="add_shop_category"
                        return-object
                        outlined
                      ></v-select>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12" style="margin-top: -20px">
                      <v-select
                        v-model="select_object"
                        :items="object_category"
                        :rules="rules"
                        item-text="obj_name"
                        label="အမျိုးအစား"
                        @click="add_object_category"
                        return-object
                        outlined
                      ></v-select>
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
                        @click="add_to_sql"
                        >Add
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-form>
              </v-card-text>
            </v-card>
          </div>
        </v-col>

        <!--Page 2-->
        <v-col cols="8">
          <div id="page2">
            <!--Jia Yi Name List-->
            <v-card outlined>
              <v-data-table
                :headers="headers"
                :items="jia_yi_list"
                :search="search"
                item-key="idname"
                class="elevation-1"
                style="margin-top: 30px"
              >
                <!-- Search Jia Yi Name -->
                <template v-slot:top>
                  <v-text-field
                    v-model="search"
                    label="Search Jia Yi Name"
                    class="mx-4"
                  ></v-text-field>
                </template>
              </v-data-table>
            </v-card>
          </div>

          <!-- <div id="page2" style="margin-top: 30px">
            <v-card outlined>
              <v-data-table
                :headers="headers"
                :items="jia_yi_list"
                item-key="idname"
                class="elevation-1"
                :search="search"
                style="margin-top: 30px"
              >
                <template v-slot:top>
                  <v-text-field
                    v-model="search"
                    label="Search Jia Yi Name"
                    class="mx-4"
                  ></v-text-field>
                </template>
              </v-data-table>
            </v-card>
          </div> -->
        </v-col>
      </v-row>
    </v-container>
    <pre>select_object:{{ select_object }}</pre>
  </v-app>
</template>

<script>
import axios from "axios";
export default {
  name: "jia_yi_category",
  data() {
    return {
      select_level_1: "",
      level_1: [],

      select_level_2: "",
      level_2: [],

      select_level_3: "",
      level_3: [],

      level_4: [],

      select_shop: "",
      shop_category: [],

      select_object: "",
      //   select_object: {

      //   },
      object_category: [],

      //   jia_yi_type: [
      //     // { id: 1, name: "ဆိုင်" },
      //     // { id: 2, name: "ဆိုဒ်" },
      //     // { id: 3, name: "ဆောက်လုပ်ရေး" },
      //     // { id: 4, name: "အခြား" },
      //   ],
      //   select_type: "",

      valid: false,

      jia_yi_name: {
        id: "",
        jia_yi_idname: "",
        jia_yi_mm_name: "",
      },

      rules: [(v) => !!v || "ကွက်လပ်မထားရပါ။"],

      jia_yi_list: [],
      search: "",
    };
  },
  watch: {
    select_level_1(value) {
      //   console.log(value);
      this.add_level_(value);
    },
    select_level_2(value) {
      //   console.log(value);
      this.add_level_(value);
    },
    select_level_3(value) {
      //   console.log(value);
      this.add_level_(value);
    },
  },
  created: function () {
    this.load_data();
  },
  computed: {
    headers() {
      return [
        { text: "ကုဒ်နံပါတ်", align: "start", value: "idname" },
        { text: "နာမည်", value: "mm_name" },
        { text: "မြို့", value: "township_name" },
        { text: "အမျိုးအစား", value: "type_name" },
        { text: "status", value: "status" },
      ];
    },
  },
  methods: {
    load_data() {
      const path = this.$api + "/jia_yi_info_api_v2";
      axios
        .get(path)
        .then((res) => {
          this.jia_yi_list = [res.data][0];
          //   console.log(this.jia_yi_list)
        })
        .catch((error) => {
          console.error(error);
        });
    },
    enter_jia_yi_mm_name() {
      this.jia_yi_name.jia_yi_idname =
        this.jia_yi_name.jia_yi_idname.toUpperCase();
      console.log("load_data_jia_yi_name");
      var send_info = {
        variable: this.jia_yi_name.jia_yi_idname,
      };
      const path = this.$api + "/jia_yi_info_api_v2";
      axios
        .post(path, send_info)
        .then((res) => {
          this.jia_yi_name.id = res.data.id;
          this.jia_yi_name.jia_yi_mm_name = res.data.mm_name;
          //   console.log(res.data);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    delete_customer_id() {
      this.jia_yi_name.jia_yi_mm_name = "";
    },

    // load shop
    add_shop_category() {
      console.log("add_shop_category");
      var send_info = {
        variable: 0,
      };
      console.log(send_info);
      const path = this.$api + "/jia_yi_info_api_v2";
      axios
        .post(path, send_info)
        .then((res) => {
          this.shop_category = [res.data][0];
        })
        .catch((error) => {
          console.error(error);
        });
    },

    // load object
    add_object_category() {
      console.log("add_object_category");
      var send_info = {
        variable: -1,
      };
      console.log(send_info);
      const path = this.$api + "/jia_yi_info_api_v2";
      axios
        .post(path, send_info)
        .then((res) => {
          this.object_category = [res.data][0];
        })
        .catch((error) => {
          console.error(error);
        });
    },

    //   After Click
    add_level_1() {
      console.log("add_level_1");
      var send_info = {
        id: 1,
        c_id: 0,
        level: 1,
      };
      //   console.log(send_info.variable);
      const path = this.$api + "/jia_yi_info_api_v2";
      axios
        .post(path, send_info)
        .then((res) => {
          this.level_1 = [res.data][0];
          //   console.log(this.level_1);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    // watch
    add_level_(value) {
      //   console.log("add_level_");
      var send_info = value;
      //   console.log(value);
      if (value == "" || value == null) {
        // console.log("empty_level");
      } else {
        const path = this.$api + "/jia_yi_info_api_v2";
        axios
          .post(path, send_info)
          .then((res) => {
            // console.log(send_info.level);
            if (send_info.level == 1) {
              this.level_2 = [res.data][0];
              //   console.log(this.level_2);
            } else if (send_info.level == 2) {
              this.level_3 = [res.data][0];
              //   console.log(this.level_3);
            } else {
              this.level_4 = [res.data][0];
              //   console.log(this.level_4);
            }
          })
          .catch((error) => {
            console.error(error);
          });
      }
    },

    // After Click : Customer Type
    add_jia_yi_type() {
      console.log("add_jia_yi_type");
      var send_info = {
        variable: 0,
      };
      console.log(send_info);
      const path = this.$api + "/jia_yi_info_api_v2";
      axios
        .post(path, send_info)
        .then((res) => {
          this.jia_yi_type = [res.data][0];
          //   console.log(this.jia_yi_type);
        })
        .catch((error) => {
          console.error(error);
        });
    },

    // After Click : Update : Add To SQL
    add_to_sql() {
      const valid = this.$refs.category_form.validate();
      console.log(valid);
      console.log("GO");
      if (valid === true) {
        console.log("GO");
        const category_form = {
          id: this.jia_yi_name.id,
          idname: this.jia_yi_name.jia_yi_idname,
          mm_name: this.jia_yi_name.jia_yi_mm_name,
          shop: this.select_shop.id,
          //   if else
          type: [
            {
              obj_id: this.select_object.obj_id,
            },
          ],
          //   township: this.select_level_3.id,
          //   type: this.select_type.id,
          //   state: this.select_level_1.name,
          //   district: this.select_level_2.name,
          //   township: this.select_level_3.name,
        };
        console.log(category_form);
        const path = this.$api + "/jia_yi_info_api_v2";
        axios
          .put(path, category_form)
          .then((res) => {
            console.log(res);
            this.load_data();
          })
          .catch((error) => {
            console.error(error);
          });
        console.log(category_form);
        this.$refs.category_form.reset();
      } else {
        console.log("ERROR");
      }
    },
  },
};
</script>