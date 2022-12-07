import { createWebHistory, createRouter } from "vue-router";

const routes =  [
  {
    path: "/",
    alias: "/locations",
    name: "locations",
    component: () => import("./components/LocationList")
  }
  , {
    path: "/locations/:id/",
    name: "location-details",
    component: () => import("./components/LocationDetail")
  }
  // , {
  //   path: "/add",
  //   name: "add",
  //   component: () => import("./components/AddLocation")
  // }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;