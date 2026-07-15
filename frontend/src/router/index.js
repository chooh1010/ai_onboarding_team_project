import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ContentListView from '../views/ContentListView.vue'
import ContentDetailView from '../views/ContentDetailView.vue'
import PostListView from '../views/PostListView.vue'
import PostDetailView from '../views/PostDetailView.vue'
import PostWriteView from '../views/PostWriteView.vue'
import PostEditView from '../views/PostEditView.vue'
import DataSourceView from '../views/DataSourceView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/explore', component: ContentListView },
  { path: '/contents/:contentId', component: ContentDetailView },
  { path: '/community', component: PostListView },
  { path: '/community/write', component: PostWriteView },
  { path: '/community/:postId', component: PostDetailView },
  { path: '/community/:postId/edit', component: PostEditView },
  { path: '/data-source', component: DataSourceView },
]

export default createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})
