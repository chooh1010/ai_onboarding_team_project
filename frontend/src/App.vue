<script setup>
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
import ChatFloatingButton from './components/chat/ChatFloatingButton.vue'
</script>

<template>
  <div class="app-shell">
    <AppHeader />
    <main>
      <RouterView />
    </main>
    <AppFooter />
    <ChatFloatingButton />
  </div>
</template>
