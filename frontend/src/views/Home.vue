<template>
  <div class="home-container">
    <div class="header-section">
      <h1 class="page-title">🤖 AI 智能查询代理</h1>
      <p class="page-subtitle">基于 ReAct 范式，为您解答一切实时问题</p>
    </div>

    <a-card class="form-card" :bordered="false">
      <a-form layout="vertical">
        <a-form-item>
          <template #label>
            <span class="form-label">您想查询什么？</span>
          </template>
          <a-textarea
            v-model:value="question"
            placeholder="例如：帮我查一下最近有什么好看的科幻电影？或者查一下苏州明天的天气？"
            :rows="4"
            class="custom-textarea"
            :disabled="loading"
          />
        </a-form-item>

        <a-form-item>
          <a-button
            type="primary"
            size="large"
            class="submit-button"
            :loading="loading"
            block
            @click="handleSubmit"
          >
            <template v-if="!loading">
              🚀 开始智能查询
            </template>
            <template v-else>
              正在思考中... 请稍候
            </template>
          </a-button>
        </a-form-item>
      </a-form>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
// 注意这里：引入了咱们刚写好的 api.ts 中的函数
import { sendQuestion } from '@/services/api' 

const router = useRouter()
const question = ref('')
const loading = ref(false)

const handleSubmit = async () => {
  if (!question.value.trim()) {
    message.warning('请先输入您的问题哦！')
    return
  }

  loading.value = true
  
  try {
    // 使用 api.ts 中的封装函数，不用再关心 axios 了
    const responseData = await sendQuestion({ question: question.value })

    if (responseData.success) {
      // 把后端返回的答案存进浏览器临时缓存，供 Result.vue 使用
      sessionStorage.setItem('agentAnswer', responseData.answer)
      message.success('查询成功！正在跳转...')
      
      // 跳转到结果页
      router.push('/result')
    } else {
      message.error(responseData.answer || '查询失败，请重试')
    }
  } catch (error: any) {
    console.error(error)
    message.error('网络错误，请确保后端服务已启动！')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  /* 绿色清新渐变背景 */
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

.form-card {
  width: 100%;
  max-width: 800px;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(34, 197, 94, 0.1);
  background: rgba(255, 255, 255, 0.98) !important;
  padding: 20px;
}

.form-label {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.custom-textarea {
  border-radius: 12px;
  border: 2px solid #e8e8e8;
  font-size: 16px;
  padding: 12px;
  transition: all 0.3s ease;
}

.custom-textarea:hover,
.custom-textarea:focus {
  border-color: #22c55e;
  box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1);
}

.submit-button {
  height: 56px;
  border-radius: 28px;
  font-size: 18px;
  font-weight: 600;
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  border: none;
  box-shadow: 0 8px 24px rgba(34, 197, 94, 0.4);
  margin-top: 10px;
}

.submit-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(34, 197, 94, 0.5);
}
</style>