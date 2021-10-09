<template>
  <v-app>
    <v-container fluid style="margin-top: 10px; margin-left: 20px">
      <v-row>
        <v-col cols="12">
          <!--Page 1-->
          <div id="page1">
            <!--KT Parameter Form-->
            <v-card>
              <v-card-title class="headline"> KT Parameter </v-card-title>
              <v-card-text>
                <v-form
                  ref="kt_parameter_form"
                  v-model="valid1"
                  style="margin-top: 5px; margin-bottom: -20px"
                >
                  <v-row>
                    <v-col cols="3">
                      <v-select
                        v-model="select_product_type_page1"
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
                    <v-col cols="2">
                      <v-text-field
                        label="Duty Ratio"
                        v-model="duty_ratio"
                        :rules="rules"
                        outlined
                      ></v-text-field>
                    </v-col>
                    <v-col cols="2">
                      <v-text-field
                        label="Percentage"
                        v-model="percentage"
                        :rules="rules"
                        @keyup.enter="add_to_sql_kt_price"
                        outlined
                      ></v-text-field>
                    </v-col>
                    <!--Add To Sql Btn-->
                    <v-col cols="2" style="margin-top: 5px">
                      <v-btn
                        rounded
                        large
                        block
                        :disabled="!valid1"
                        color="blue-grey lighten-2"
                        @click="add_to_sql_kt_price"
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
      </v-row>
      <v-row>
        <!--Page 2-->
        <v-col cols="12">
          <div id="page2">
            <!--KT Price-->
            <v-card outlined>
              <!-- Edit Dialog -->
              <v-dialog v-model="edit_dialog" persistent max-width="250">
                <v-card>
                  <v-form ref="kt_parameter_update_form" v-model="valid2">
                    <v-card-title class="headline">
                      <!-- Edit Name -->
                    </v-card-title>
                    <v-card-text>
                      <v-row
                        ><v-col cols="12">
                          <v-text-field
                            v-model="edit_list.duty_ratio"
                            :rules="rules"
                            label="ဂျူတီအချိုး"
                            outlined
                            autofocus
                          ></v-text-field>
                        </v-col>
                      </v-row>
                      <v-row style="margin-top: -15px"
                        ><v-col cols="12">
                          <v-text-field
                            v-model="edit_list.percentage"
                            :rules="rules"
                            label="ရာခိုင်နှုန်း"
                            @keyup.enter="updated"
                            outlined
                            autofocus
                          ></v-text-field>
                        </v-col>
                      </v-row>
                    </v-card-text>
                    <v-card-actions style="margin-top: -25px">
                      <v-spacer></v-spacer>
                      <v-btn
                        color="black darken-1"
                        text
                        @click="edit_dialog = false"
                      >
                        ပယ်ဖျက်
                      </v-btn>
                      <v-btn
                        color="green darken-1"
                        text
                        :disabled="!valid2"
                        @click="updated()"
                      >
                        အတည်ပြု
                      </v-btn>
                    </v-card-actions>
                  </v-form>
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

                <!-- duty_price 小数点后2位数 -->
                <template v-slot:item.duty_price="{ item }">
                  <span class="money">{{ item.duty_price | numFilter }}</span>
                </template>

                <!-- kt_price 小数点后2位数 -->
                <template v-slot:item.kt_price="{ item }">
                  <span class="money">{{ item.kt_price | numFilter }}</span>
                </template>

                <!-- Edit Btn -->
                <template v-slot:item.icon="{ item }">
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
    <pre>select_product_type_page2:{{ select_product_type_page2 }}</pre>
    <pre>edit_list:{{ edit_list }}</pre>
    <!-- <pre>duty_list:{{ duty_list }}</pre> -->
  </v-app>
</template>

<script>
import axios from "axios";
import moment from "moment-timezone";
export default {
  data() {
    return {
      valid1: false,
      valid2: false,

      rules: [(v) => !!v || "ကွက်လပ်မထားရပါ။"],

      //   product_type_list: [],
      // select_type_name: "",

      //   duty_list: [],
      //   select_duty_name: "",

      // Select Product Type
      product_type_list: [],
      select_product_type_page1: "",
      select_product_type_page2: "",
      duty_ratio: "",
      percentage: "",

      // Search Product
      search: "",
      product_list: [],

      //   Edit Dialog
      edit_dialog: false,
      edit_list: "",

      // Current Time
      currentTime: "",
    };
  },
  watch: {
    //   Select : product_type
    select_product_type_page2() {
      console.log(this.select_product_type_page2);
      this.product_type_page2();
    },
  },
  created: function () {
    this.load_data();
  },
  filters: {
    numFilter(value) {
      // 截取当前数据到小数点后两位
      let realVal = parseFloat(value).toFixed(1);
      return realVal;
    },
  },
  computed: {
    headers() {
      return [
        // { text: "ကုဒ်နံပါတ်", align: "start", value: "datetime" },
        { text: "ကုဒ်နံပါတ်", value: "idname" },
        { text: "နာမည်", value: "mm_name" },
        { text: "Detail", value: "d_name" },
        { text: "Weight", value: "weight" },
        // { text: "အမျိုးအစား", value: "type_name" },
        { text: "duty_price", value: "duty_price" },
        { text: "ဂျူတီအချိုး", value: "duty_ratio" },
        { text: "ရာခိုင်နှုန်း", value: "percentage" },
        // { text: "s_price", value: "s_price" },
        { text: "kt_price", value: "price" },
        { text: "Icon", value: "icon" },
      ];
    },
  },
  methods: {
    load_data() {
      var send_info = {
        variable: "",
      };
      const path = this.$api + "/price_parameter_api";
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
    // Select: product_type
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
    add_to_sql_kt_price() {
      console.log("GO");

	  console.log(moment.tz.guess()); // 如果你不知道你自己当前所在地的时区，请使用此代码查看.
      const dateWithZone1 = moment(new Date()).tz("Asia/Rangoon");
      const RangoonTimezoneDate = dateWithZone1.format("YYYY-MM-DD kk:mm:ss");
      console.log(RangoonTimezoneDate);

      var send_info = {
        variable: -1,
		datetime: RangoonTimezoneDate,
        duty_ratio: this.duty_ratio,
        percentage: this.percentage,
      };
      console.log(send_info);
      const path = this.$api + "/price_parameter_api";
      axios
        .put(path, send_info)
        .then((res) => {
          console.log([res.data][0]);
          this.load_data();
        })
        .catch((error) => {
          console.error(error);
        });
      this.$refs.kt_parameter_form.reset();
    },

    // select product type page2
    product_type_page2() {
      var send_info = {
        type: this.select_product_type_page2.type,
      };
      console.log(send_info.type);
      const path = this.$api + "/price_parameter_api";
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

    //   EDIT
    edit_dialog_(item) {
      // edit_list 這個list 是爲了更新到數據表而存在
      console.log(item);
      this.edit_list = {
        id: item.id,
        duty_ratio: item.duty_ratio,
        percentage: item.percentage,
      };
      this.edit_dialog = true;
    },
    // Duty Ratio / Percentage
    updated() {
      console.log(moment.tz.guess()); // 如果你不知道你自己当前所在地的时区，请使用此代码查看.
      const dateWithZone1 = moment(new Date()).tz("Asia/Rangoon");
      const RangoonTimezoneDate = dateWithZone1.format("YYYY-MM-DD kk:mm:ss");
      console.log(RangoonTimezoneDate);
      var send_info = {
        variable: -2,
        id: this.edit_list.id,
        datetime: RangoonTimezoneDate,
        duty_ratio: this.edit_list.duty_ratio,
        percentage: this.edit_list.percentage,
      };
      console.log(send_info);
      const path = this.$api + "/price_parameter_api";
      axios
        .put(path, send_info)
        .then((res) => {
          console.log(res.data);
          if (this.select_product_type_page2 == "") {
            this.load_data();
          } else {
            this.product_type_page2();
          }
        })
        .catch((error) => {
          console.error(error);
          console.log("update error");
        });
      this.edit_dialog = false;
      this.$refs.kt_parameter_form.reset();
    },
  },
};
</script>

<style>
</style>