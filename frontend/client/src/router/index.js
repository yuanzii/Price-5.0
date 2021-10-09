import Vue from "vue";
import VueRouter from "vue-router";
// import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes = [

	// Home
	{
		path: "/",
		name: "home",
		component: () =>
			import("../views/home.vue"),
	},

	// Jia Yi Management
	{
		path: "/jia_yi_category",
		name: "jia_yi_category",
		component: () =>
			import("../views/customer_management/jia_yi_category.vue"),
	},
	{
		path: "/jia_yi_type",
		name: "jia_yi_type",
		component: () =>
			import("../views/customer_management/jia_yi_type.vue"),
	},
	{
		path: "/jia_yi_info",
		name: "jia_yi_info",
		component: () =>
			import("../views/customer_management/jia_yi_info.vue"),
	},

	// Product Management
	{
		path: "/product_info",
		name: "product_info",
		component: () =>
			import("../views/product_management/product_info.vue"),
	},
	// KT Price Parameter
	{
		path: "/kt_price_parameter",
		name: "kt_price_parameter",
		component: () =>
			import("../views/product_management/kt_price_parameter.vue"),
	},
	// {
	// 	path: "/duty",
	// 	name: "duty",
	// 	component: () =>
	// 		import("../views/product_management/duty.vue"),
	// },
	//   {
	//     path: "/product_category",
	//     name: "Product_Category",
	//     component: () =>
	//       import("../views/product_category.vue"),
	//   },
	{
		path: '/product_category', name: 'Product_Category', component: () =>
			import("../views/product_management/product_category.vue"), children: [
				{
					path: 'level_1', name: 'Level_1', component: () =>
						import("../views/product_management/level_1.vue")
				},
				{
					path: 'level_2', name: 'Level_2', component: () =>
						import("../views/product_management/level_2.vue")
				},
				{
					path: 'level_3', name: 'Level_3', component: () =>
						import("../views/product_management/level_3.vue")
				},
				// {
				// 	path: 'level_2/:id', name: 'level_2', component: () =>
				// 		import("../views/level_2.vue")
				// },
				// {
				// 	path: '/product_category', redirect: '/product_category'
				// },
				//在children的后面加一个redirect：'/想要默认展示的子路由名字'

			]

	},
	// { path: '*', redirect: '/' }

];

const router = new VueRouter({
	routes,
});

export default router;
