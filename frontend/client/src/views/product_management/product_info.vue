<template>
  <v-app>
    <v-container fluid style="margin-top: 10px">
      <v-row>
        <!--Page 1-->
        <v-col cols="3">
          <div id="page1">
            <!--Add Product Type To Sql-->
            <v-card outlined>
              <v-card-title>
                <span class="headline"> ထုတ်ကုန်အမျိုးအစားခွဲခြား </span>
              </v-card-title>
              <v-card-text>
                <!--Product Type Form-->
                <v-form
                  ref="category_form"
                  v-model="valid1"
                  style="margin-top: 5px"
                >
                  <v-row
                    ><v-col cols="12">
                      <v-text-field
                        label="ကုဒ်နံပါတ်"
                        v-model="product.idname"
                        :rules="rules"
                        @keyup.enter="enter_product_mm_name"
                        @keyup.delete="delete_product_id"
                        outlined
                        autofocus
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row
                    ><v-col cols="12" style="margin-top: -20px">
                      <v-text-field
                        label="နာမည်"
                        v-model="product.mm_name"
                        :rules="rules"
                        outlined
                        readonly
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row
                    ><v-col cols="12" style="margin-top: -20px">
                      <v-text-field
                        label="Detail"
                        v-model="product.d_name"
                        outlined
                        readonly
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <!-- Level-1 -->
                  <v-row>
                    <v-col cols="12" style="margin-top: -20px">
                      <v-select
                        v-model="select_level_1"
                        :items="level_1"
                        :rules="rules"
                        item-text="name"
                        label="ထုပ်ကုန်အမျိုးအစား Level-1"
                        @click="add_level_1"
                        return-object
                        outlined
                      ></v-select>
                    </v-col>
                  </v-row>
                  <!-- Level-2 -->
                  <v-row>
                    <v-col cols="12" style="margin-top: -20px">
                      <v-select
                        v-model="select_level_2"
                        :items="level_2"
                        :rules="rules"
                        item-text="name"
                        label="ထုပ်ကုန်အမျိုးအစား Level-2"
                        return-object
                        outlined
                      ></v-select>
                    </v-col>
                  </v-row>
                  <v-row>
                    <!-- Level-3 -->
                    <v-col cols="12" style="margin-top: -20px">
                      <v-select
                        v-model="select_level_3"
                        :items="level_3"
                        :rules="rules"
                        item-text="name"
                        label="ထုပ်ကုန်အမျိုးအစား Level-3"
                        return-object
                        outlined
                      ></v-select>
                    </v-col>
                  </v-row>

                  <!--Product Type Form Btn-->
                  <v-row>
                    <v-col
                      class="pt-0"
                      style="margin-top: -10px; margin-bottom: 15px"
                    >
                      <v-btn
                        rounded
                        large
                        block
                        :disabled="!valid1"
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

        <!--Page 2.1-->
        <v-col cols="9">
          <!--Page 2.1-->
          <div id="page2.1">
            <!--Duty Type Form-->
            <v-card>
              <v-card-title class="headline"> ဂျူတီခွဲခြား </v-card-title>
              <v-card-text>
                <v-form
                  ref="duty_form"
                  v-model="valid2"
                  style="margin-top: 5px; margin-bottom: -20px"
                >
                  <v-row>
                    <v-col cols="4">
                      <v-select
                        v-model="select_product_type"
                        :items="product_type_list"
                        :rules="rules"
                        item-text="type_name"
                        item-value="id"
                        label="ထုတ်ကုန်အမျိုးအစား"
                        @click="product_type"
                        return-object
                        outlined
                      ></v-select>
                    </v-col>
                    <v-col cols="4">
                      <v-select
                        v-model="select_duty_type"
                        :items="duty_type_list"
                        :rules="rules"
                        item-text="mm_name"
                        item-value="id"
                        label="ဂျူတီအုပ်စု"
                        @click="duty_type"
                        return-object
                        outlined
                      ></v-select>
                    </v-col>
                    <!--Duty Type Form Btn-->
                    <v-col cols="2" style="margin-top: 5px">
                      <v-btn
                        rounded
                        large
                        block
                        :disabled="!valid2"
                        color="blue-grey lighten-2"
                        @click="add_to_sql_duty"
                      >
                        Add
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-form>
              </v-card-text>
            </v-card>
          </div>

          <!--Page 2.2-->
          <div id="page2.2" style="margin-top: 25px">
            <!--Product List-->
            <v-card outlined>
              <!-- Edit Dialog -->
              <v-dialog v-model="edit_dialog" persistent max-width="290">
                <v-card>
                  <v-card-title class="headline">
                    <!-- Edit Weight -->
                  </v-card-title>
                  <v-card-text>
                    <v-row
                      ><v-col cols="12" style="margin-top: 15px">
                        <v-text-field
                          v-model="edit_list.weight"
                          :rules="rules"
                          label="ထုတ်ကုန်အလေးချိန်"
                          @keyup.enter="updated()"
                          outlined
                          autofocus
                        ></v-text-field>
                      </v-col>
                    </v-row>
                  </v-card-text>
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
                :items="product_list"
                :search="search"
                :items-per-page="5"
                item-key="idname"
                class="elevation-1"
                style="margin-top: 30px"
              >
                <template v-slot:top>
                  <v-row>
                    <v-col cols="3">
                      <v-select
                        v-model="select_product_type_page2"
                        class="mx-5"
                        :items="product_type_list"
                        :rules="rules"
                        item-text="type_name"
                        item-value="id"
                        label="ထုတ်ကုန်အမျိုးအစား"
                        @click="product_type"
                        return-object
                      ></v-select>
                    </v-col>
                    <v-col cols="8">
                      <v-text-field
                        v-model="search"
                        label="Search"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </template>

                <template v-slot:item.icon="{ item }">
                  <!-- Btn -->
                  <v-btn
                    style="cursor: move"
                    icon
                    class="sortHandle"
                    @click="edit_dialog_(item)"
                  >
                    <v-icon>edit</v-icon>
                  </v-btn>
                </template>
              </v-data-table>
            </v-card>
          </div>
        </v-col>
      </v-row>
    </v-container>
    <pre class="ml-10">select_level_1:{{ select_level_1 }}</pre>
    <pre class="ml-10">select_level_2:{{ select_level_2 }}</pre>
    <pre class="ml-10">select_level_3:{{ select_level_3 }}</pre>
    <pre class="ml-10">valid1:{{ valid1 }}</pre>
    <pre class="ml-10">valid2:{{ valid2 }}</pre>
  </v-app>
</template>

<script>
import axios from "axios";
export default {
  name: "about",
  data() {
    return {
      //   Product Type Form
      valid1: false,
      //   Duty Type Form
      valid2: false,

      product: {
        id: "",
        idname: "",
        mm_name: "",
        d_name: "",
      },

      rules: [(v) => !!v || "ကွက်လပ်မထားရပါ။"],

      // select Product Category Level
      level_1: [],
      select_level_1: "",

      level_2: [],
      select_level_2: "",

      level_3: [],
      select_level_3: "",

      // select Product Type
      product_type_list: [],
      select_product_type: "",
      select_product_type_page2: "",

      // select Duty Type
      duty_type_list: [],
      select_duty_type: "",

      //   Search
      search: "",
      product_list: [],

      //   Edit Dialog
      edit_dialog: false,
      edit_list: "",
    };
  },
  watch: {
    // Select Product Category
    select_level_1(value) {
      this.select_level_2 = "";
      this.select_level_3 = "";
      this.add_level_(value);
    },
    select_level_2(value) {
      this.add_level_(value);
    },
    select_level_3(value) {
      console.log(value);
    },

    // Select Duty Type
    select_type_name(value) {
      console.log(value);
      this.select_duty_type = "";
    },

    //   Select : product_type_page2
    select_product_type_page2() {
      console.log(this.select_product_type_page2);
      this.product_type_page2();
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
        { text: "Detail", value: "d_name" },
        { text: "အလေးချိန်(kg)", value: "weight" },
        { text: "အမျိုးအစား", value: "type_name" },
        { text: "ဂျူတီအမျိုးအစား", value: "duty_mm_name" },
        { text: "status", value: "status" },
        { text: "Icon", value: "icon" },
      ];
    },
  },
  methods: {
    load_data() {
      var send_info = {
        variable: -1,
      };
      const path = this.$api + "/product_info_api";
      axios
        .post(path, send_info)
        .then((res) => {
          this.product_list = [res.data][0];
          console.log(this.product_list);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    // select product type page2
    product_type_page2() {
      var send_info = {
        variable: -1,
        type: this.select_product_type_page2.type,
      };
      console.log(send_info.type);
      const path = this.$api + "/product_info_api";
      axios
        .post(path, send_info)
        .then((res) => {
          this.product_list = [res.data][0];
          console.log(this.product_list);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    // load_data() {
    //   const path = this.$api + "/product_info_api";
    //   axios
    //     .get(path)
    //     .then((res) => {
    //       this.product_list = [res.data][0];
    //       //   console.log(this.product_list);
    //     })
    //     .catch((error) => {
    //       console.error(error);
    //     });
    // },

    enter_product_mm_name() {
      this.product.idname = this.product.idname.toUpperCase();
      console.log("load_data");
      var send_info = {
        variable: this.product.idname,
      };
      const path = this.$api + "/product_info_api";
      axios
        .post(path, send_info)
        .then((res) => {
          this.product.id = res.data.id;
          this.product.mm_name = res.data.mm_name;
          this.product.d_name = res.data.d_name;
          //   console.log(res.data);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    delete_product_id() {
      this.product.mm_name = "";
    },
    //   After Click: Level_1
    add_level_1() {
      console.log("add_level_1");
      var send_info = { id: 0 };
      const path = this.$api + "/product_info_api";
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
      console.log("add_level_");
      var send_info = value;
      console.log(value);
      if (value == "" || value == null) {
        console.log("empty_level");
      } else {
        const path = this.$api + "/product_info_api";
        axios
          .post(path, send_info)
          .then((res) => {
            if (send_info.level == 1) {
              this.level_2 = [res.data][0];
              console.log(this.level_2);
            } else {
              this.level_3 = [res.data][0];
              if (this.level_3.length == 0) {
                console.log("this.level_3.length == 0");
                this.select_level_3 = -1;
              } else {
                this.select_level_3 = "";
              }
              console.log(this.level_3);
            }
          })
          .catch((error) => {
            console.error(error);
          });
      }
    },
    // After Click : Update : Add To SQL
    add_to_sql() {
      console.log("GO");
      console.log(this.select_level_3.id);
      if (this.select_level_3.id == undefined) {
        var type_id = this.select_level_2.id;
      } else {
        type_id = this.select_level_3.id;
      }
      const category_form = {
        variable: type_id,
        id: this.product.id,
        type: type_id, //id of level_2 or Level_3
      };
      console.log(category_form.type);
      const path = this.$api + "/product_info_api";
      axios
        .put(path, category_form)
        .then((res) => {
          console.log(res.data);
          this.load_data();
          //   this.add_to_sql_duty();
        })
        .catch((error) => {
          console.error(error);
        });
      this.$refs.category_form.reset();
    },

    // Click: To Get product_type
    product_type() {
      var send_info = {
        variable: -2,
      };
      const path = this.$api + "/product_info_api";
      axios
        .post(path, send_info)
        .then((res) => {
          this.product_type_list = [res.data][0];
          console.log(this.product_type_list);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    // Click: To Get duty_type
    duty_type() {
      var send_info = {
        variable: -3,
      };
      const path = this.$api + "/product_info_api";
      axios
        .post(path, send_info)
        .then((res) => {
          this.duty_type_list = [res.data][0];
          //   console.log(this.duty_type_list);
        })
        .catch((error) => {
          console.error(error);
        });
    },

    // After Click: Update Duty
    add_to_sql_duty() {
      console.log("GO");
      var send_info = {
        variable: -2,
        type: this.select_product_type.type, // id of product type
        duty: this.select_duty_type.id, // id of duty
      };
      console.log(send_info.type);
      const path = this.$api + "/product_info_api";
      axios
        .put(path, send_info)
        .then((res) => {
          console.log([res.data][0]);
          this.load_data();
        })
        .catch((error) => {
          console.error(error);
        });
      this.$refs.duty_form.reset();
    },

    //   EDIT
    edit_dialog_(item) {
      // edit_list 這個list 是爲了更新到數據表而存在
      this.edit_list = {
        id: item.id,
        weight: item.weight,
      };
      this.edit_dialog = true;
    },
    // Weight
    updated() {
      var send_info = {
        variable: -1,
        id: this.edit_list.id,
        weight: this.edit_list.weight,
      };
      //   console.log(send_info);
      const path = this.$api + "/product_info_api";
      axios
        .put(path, send_info)
        .then((res) => {
          console.log(res.data);
          if (this.select_product_type_page2 == "") {
            this.load_data();
          } else {
            this.product_type_page2();
          }
          //   this.edit_list = "";
        })
        .catch((error) => {
          console.error(error);
          console.log("update error");
        });
      this.edit_dialog = false;
    },
  },
};
</script>