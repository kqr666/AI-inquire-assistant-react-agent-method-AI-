<template>
  <div class="result-container">
    <div class="header-section">
      <h1 class="page-title">📋 智能查询报告</h1>
      <p class="page-subtitle">AI Agent 为您生成的专属解答</p>
    </div>

    <a-card class="result-card" :bordered="false">
      <!-- 如果有答案，展示答案 -->
      <div v-if="answer" class="answer-content">
        <!-- 用 pre-wrap 保留大模型输出时的换行符 -->
        <div class="answer-text">{{ answer }}</div>
      </div>

      <!-- 如果没拿到答案（比如强行通过网址进来的） -->
      <div v-else class="empty-state">
        <a-empty description="暂无查询结果，请先返回首页提问" />
      </div>

      <div class="action-footer">
        <a-button type="primary" size="large" class="back-button" @click="goBack">
          🔙 返回首页继续查询
        </a-button>
      </div>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const answer = ref('')

onMounted(() => {
  // 页面一加载，立刻去浏览器的临时仓库把答案掏出来
  const cachedAnswer = sessionStorage.getItem('agentAnswer')
  if (cachedAnswer) {
    answer.value = cachedAnswer
  }
})

const goBack = () => {
  router.push('/')
}
</script>

<style scoped>
.result-container {
  min-height: 100vh;
  /* 和首页保持一致的绿色清新渐变 */
  background: linear-gradient(135deg, #e0f7fa 0%, #c8e6c9 100%);
  padding: 60px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.header-section {
  text-align: center;
  margin-bottom: 40px;
}

.page-title {
  font-size: 42px;
  font-weight: 800;
  color: #1B5E20;
  margin-bottom: 12px;
  letter-spacing: 2px;
}

.page-subtitle {
  font-size: 18px;
  color: #2E7D32;
}

.result-card {
  width: 100%;
  max-width: 900px;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(34, 197, 94, 0.1);
  background: rgba(255, 255, 255, 0.98) !important;
  padding: 20px;
}

.answer-content {
  background: #f8fafc;
  border-radius: 12px;
  padding: 24px;
  border: 1px solid #e2e8f0;
  margin-bottom: 30px;
}

.answer-text {
  font-size: 16px;
  line-height: 1.8;
  color: #333;
  /* 极其重要：保留大模型生成的换行符，否则全挤在一块了 */
  white-space: pre-wrap; 
  word-wrap: break-word;
}

.empty-state {
  padding: 40px 0;
  text-align: center;
}

.action-footer {
  text-align: center;
  margin-top: 20px;
}

.back-button {
  height: 50px;
  border-radius: 25px;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  border: none;
  box-shadow: 0 8px 24px rgba(34, 197, 94, 0.3);
  padding: 0 40px;
}

.back-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(34, 197, 94, 0.4);
}
</style>