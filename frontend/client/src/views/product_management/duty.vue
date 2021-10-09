<template>
  <v-app>
    <v-container fluid style="margin-top: 10px; margin-left: 20px">
      <v-row>
        <v-col cols="3">
          <!--Page 1-->
          <div id="page1">
            <!--Duty List-->
            <v-card>
              <v-card-title class="headline"> Insert Duty </v-card-title>
              <v-card-text>
                <v-form ref="duty_form" v-model="valid">
                  <v-row>
                    <v-col cols="12" style="margin-top: 15px">
                      <v-select
                        v-model="select_type_name"
                        :items="type_list"
                        :rules="rules"
                        item-text="type_name"
                        item-value="id"
                        label="ထုတ်ကုန်အမျိုးအစား"
                        @click="product_type_list"
                        return-object
                        outlined
                      ></v-select>
                    </v-col>
                    <v-col cols="12" style="margin-top: -20px">
                      <v-select
                        v-model="select_duty_name"
                        :items="duty_list"
                        :rules="rules"
                        item-text="mm_name"
                        item-value="id"
                        label="အုပ်စုအမည်"
                        @click="duty_type_list"
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
                      >
                        Add
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-form>
              </v-card-text>
            </v-card>
          </div>
          <!--Page 2-->
          <div id="page2" style="margin-top: 10px;">
            <!--KT Parameter-->
            <v-card>
              <v-card-title class="headline"> KT Parameter </v-card-title>
              <v-card-text>
                <v-form ref="kt_parameter_form" v-model="valid">
                  <v-row>
                    <v-col cols="12" style="margin-top: 15px">
                      <v-select
                        v-model="select_type_name_kt"
                        :items="type_list"
                        :rules="rules"
                        item-text="type_name"
                        item-value="id"
                        label="ထုတ်ကုန်အမျိုးအစား"
                        @click="product_type_list"
                        return-object
                        outlined
                      ></v-select>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12" style="margin-top: -20px">
                      <v-text-field
                        label="Duty Ratio"
                        v-model="duty_ratio"
                        :rules="rules"
                        outlined
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12" style="margin-top: -20px">
                      <v-text-field
                        label="Percentage"
                        v-model="percentage"
                        :rules="rules"
                        outlined
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

		<!--Page 3-->
        <v-col cols="9">
          <div id="page3">
            <!--KT Price-->
            <v-card outlined>
              <!-- Edit Dialog -->
              <v-dialog v-model="edit_dialog" persistent max-width="290">
                <v-card>
                  <v-card-title class="headline">
                    <!-- Edit Name -->
                  </v-card-title>
                  <v-card-text>
                    <!-- <v-row
                      ><v-col cols="12" style="margin-top: 15px">
                        <v-text-field
                          v-model="edit_list.weight"
                          :rules="rules"
                          label="ထုတ်ကုန်အလေးချိန်"
                          outlined
                          autofocus
                        ></v-text-field>
                      </v-col>
                    </v-row> -->
                    <v-row
                      ><v-col cols="12" style="margin-top: 15px">
                        <v-text-field
                          v-model="edit_list.percentage"
                          :rules="rules"
                          label="Percentage"
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
                item-key="idname"
                class="elevation-1"
                style="margin-top: 30px"
              >
                <template v-slot:top>
                  <v-text-field
                    v-model="search"
                    label="Search Jia Yi Name"
                    class="mx-4"
                  ></v-text-field>
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
    <!-- <pre>valid:{{ valid }}</pre> -->
    <!-- <pre>type_list:{{ type_list }}</pre>
	<pre>duty_list:{{ duty_list }}</pre> -->
  </v-app>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      valid: false,

      rules: [(v) => !!v || "ကွက်လပ်မထားရပါ။"],

      // select
      type_list: [],
      select_type_name: "",

      duty_list: [],
      select_duty_name: "",

      kt_price_type_name: [],
      select_type_name_kt: "",
      duty_ratio: "",
      percentage: "",



	  search: "",
      product_list: [],

      //   Edit Dialog
      edit_dialog: false,
      edit_list: "",
    };
  },
  watch: {
    select_type_name(value) {
      console.log(value);
      this.select_duty_name = "";
    },
    select_duty_name(value) {
      console.log(value);
    },
  },
  methods: {
    product_type_list() {
      var send_info = {
        variable: 0,
      };
      const path = this.$api + "/price_parameter_api";
      axios
        .post(path, send_info)
        .then((res) => {
          this.type_list = [res.data][0];
          this.kt_price_type_name = [res.data][0];
        })
        .catch((error) => {
          console.error(error);
        });
    },
    duty_type_list() {
      var send_info = {
        variable: "",
      };
      const path = this.$api + "/price_parameter_api";
      axios
        .post(path, send_info)
        .then((res) => {
          this.duty_list = [res.data][0];
        })
        .catch((error) => {
          console.error(error);
        });
    },
    add_to_sql() {
      const valid = this.$refs.duty_form.validate();
      console.log(valid);
      console.log("GO");
      var send_info = {
        variable: 0,
        type: this.select_type_name.type,
        duty: this.select_duty_name.id,
      };
      console.log(send_info);
      const path = this.$api + "/price_parameter_api";
      axios
        .put(path, send_info)
        .then((res) => {
          console.log([res.data][0]);
        })
        .catch((error) => {
          console.error(error);
        });
      this.$refs.duty_form.reset();
    },
    add_to_sql_kt_price() {
      const valid = this.$refs.kt_parameter_form.validate();
      console.log(valid);
      console.log("GO");
      var send_info = {
        variable: "",
        type: this.select_type_name_kt.type,
        duty_ratio: this.duty_ratio,
        percentage: this.percentage,
      };
      console.log(send_info);
      const path = this.$api + "/price_parameter_api";
      axios
        .put(path, send_info)
        .then((res) => {
          console.log([res.data][0]);
        })
        .catch((error) => {
          console.error(error);
        });
      this.$refs.kt_parameter_form.reset();
    },
  },
};
</script>

<style>
</style>