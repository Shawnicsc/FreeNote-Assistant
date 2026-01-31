<template>
  <div class="editor-page">
    <!-- 顶部工具栏（占位） -->
    <div class="editor-toolbar">
      <span class="title">当前文档</span>

      <div class="actions">
        <el-button size="small">总结</el-button>
        <el-button size="small">润色</el-button>
        <el-button size="small">UML</el-button>
        <el-button size="small" @click="openFile">打开文件</el-button>
        <el-button
            size="small"
            type="primary"
            :disabled="!documentStore.isDirty"
            @click="saveFile"
        >
        保存
        </el-button>

      </div>
    </div>

    <!-- 编辑主区域 -->
    <div class="editor-main">
      <div class = "editor-page">
        <MarkdownEditor v-model="documentStore.content"/>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import MarkdownEditor from '@/editor/MarkdownEditor.vue'
import { documentStore, setDocumentContent } from '@/document/document.store'
import { watch } from 'vue'
import { replaceDocumentContent } from '@/document/document.store'
import { ElMessage } from 'element-plus'

let currentFileHandle: any = null

watch(
  () => documentStore.content,
  (val) => {
    documentStore.isDirty = true
    console.log('document content:', val)
    console.log('isDirty:', documentStore.isDirty)
  }
)
async function openFile() {
  try {
    const [fileHandle] = await (window as any).showOpenFilePicker({
      types: [
        {
          description: 'Markdown Files',
          accept: {
            'text/markdown': ['.md'],
          },
        },
      ],
      multiple: false,
    })

    const file = await fileHandle.getFile()
    const content = await file.text()
    currentFileHandle = fileHandle

    // 用“替换”方式更新文档
    replaceDocumentContent(content)
    ElMessage.success('文件已加载')

    // 可选：记录当前文件名（后续用）
    // console.log('Opened file:', file.name)
  } catch (err: any) {
    // 用户取消选择不算错误
    if (err?.name === 'AbortError') {
    // 用户取消，不提示
    ElMessage.info('已取消打开文件')
    return
  }

  ElMessage.error('文件打开失败')
  console.error(err)
  }
}

async function saveFile() {
  try {
    // 第一次保存 or 没有文件句柄
    if (!currentFileHandle) {
      currentFileHandle = await (window as any).showSaveFilePicker({
        suggestedName: 'note.md',
        types: [
          {
            description: 'Markdown Files',
            accept: {
              'text/markdown': ['.md'],
            },
          },
        ],
      })
    }

    const writable = await currentFileHandle.createWritable()
    await writable.write(documentStore.content)
    await writable.close()

    documentStore.isDirty = false

    ElMessage.success('保存成功')

  } catch (err: any) {
    if (err?.name === 'AbortError') {
        ElMessage.info('已取消保存')
        return
    }

    ElMessage.error('保存失败')
    console.error(err)
  }
}



</script>

<style scoped>
.editor-page {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 48px); /* 减去 header */
}

.editor-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 12px;
  border-bottom: 1px solid #eee;
  background: #fafafa;
}

.editor-toolbar .title {
  font-size: 13px;
  color: #666;
}
.editor-toolbar .el-button {
  font-size: 12px;
  padding: 4px 8px;
}

.editor-main {
  flex: 1;
  padding: 24px;
  background: #f6f7f9;
}

.editor-paper {
  max-width: 820px;
  background: #fff;
  padding: 24px 32px;
  border-radius: 6px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
}

.editor-placeholder {
  height: 100%;
  border: 1px dashed #ccc;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  background: #fff;
}

</style>
