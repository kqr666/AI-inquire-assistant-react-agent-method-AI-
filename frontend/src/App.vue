<template>
  <div id="app">
    <a-layout style="min-height: 100vh">
      
      <a-layout-header style="background: #22c55e; padding: 0 50px; display: flex; justify-content: center; align-items: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1)">
        <div style="color: white; font-size: 24px; font-weight: bold; letter-spacing: 2px;">
          🤖 AI 智能查询代理
        </div>
      </a-layout-header>
      
      <a-layout-content style="padding: 24px">
        <router-view />
      </a-layout-content>
      
      <a-layout-footer style="text-align: center; color: #888; background: #f8fafc;">
        2026年11月10日 | 基于 ReAct 范式的智能体应用
      </a-layout-footer>
      
    </a-layout>
  </div>
</template>

<script setup lang="ts">
</script>

<style>
#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #f1f5f9;
}
</style>