<template>
  <v-app>
    <v-container fluid style="margin-top: 10px">
      <v-row>
        <!--Page 1-->
        <v-col cols="12">
          <div id="page1">
            <!--Price List-->
            <v-card outlined>
              <v-data-table
                :headers="headers"
                :items="product_list"
                :search="search"
                item-key="idname"
                class="elevation-1"
                style="margin-top: 15px"
              >
                <template v-slot:top>
                  <v-row>
                    <v-col cols="3">
                      <v-autocomplete
                        v-model="select_product_type"
                        class="mx-5"
                        :items="product_type_list"
                        item-text="type_name"
                        item-value="id"
                        label="ထုတ်ကုန်အမျိုးအစား"
                        @click="product_type"
                        return-object
                      ></v-autocomplete>
                    </v-col>
                    <v-col cols="8">
                      <v-text-field
                        v-model="search"
                        label="Search"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </template>
                <!-- kt_price 小数点后2位数 -->
                <template v-slot:item.kt_price="{ item }">
                  <span class="money">{{ item | numFilter }}</span>
                </template>
              </v-data-table>
            </v-card>
          </div>
        </v-col>
      </v-row>
    </v-container>
    <pre>select_product_type:{{ select_product_type }}</pre>
    <pre>product_type_list:{{ product_type_list }}</pre>
  </v-app>
</template>

<script>
import axios from "axios";
export default {
  name: "about",
  data() {
    return {
      product: {
        id: "",
        idname: "",
        mm_name: "",
        d_name: "",
      },

      //   rules: [(v) => !!v || "ကွက်လပ်မထားရပါ။"],
      //   开始
      search: "",
      product_list: [],

      product_type_list: [],
      select_product_type: null,
    };
  },
  watch: {
    //   Select : product_type
    select_product_type(value) {
      console.log(value);
      if (value == null) {
        this.load_data();
      } else {
        var send_info = value;
        const path = this.$api + "/purchase_s_price_api";
        axios
          .post(path, send_info)
          .then((res) => {
            this.product_list = [res.data][0];
            console.log(this.product_list);
          })
          .catch((error) => {
            console.error(error);
          });
      }
    },
  },
  created: function () {
    this.load_data();
  },
  filters: {
    numFilter(value) {
      // 截取当前数据到小数点后两位
      let realVal = parseFloat(value.kt_price).toFixed(1);
      return realVal;
    },
  },
  computed: {
    headers() {
      return [
        { text: "ID", align: "start", value: "id" },
        { text: "ကုဒ်နံပါတ်", value: "idname" },
        { text: "နာမည်", value: "mm_name" },
        { text: "Detail", value: "d_name" },
        { text: "Weight", value: "weight" },
        { text: "S_price", value: "s_price" },
        { text: "O_price", value: "o_price" },
        { text: "KT_price", value: "kt_price" },
      ];
    },
  },
  methods: {
    load_data() {
      const path = this.$api + "/cost_ratio_api";
      axios
        .get(path)
        .then((res) => {
          this.product_list = [res.data][0];
          console.log(this.product_list);
        })
        .catch((error) => {
          console.error(error);
        });
    },

    // Click : To Get Product Type
    product_type() {
      var send_info = {
        variable: -2,
      };
      const path = this.$api + "/product_info_api";
      axios
        .post(path, send_info)
        .then((res) => {
          this.product_type_list = [res.data][0];
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>