import { reactive } from 'vue'

export interface DocumentState {
  content: string
  isDirty: boolean
}

export const documentStore = reactive<DocumentState>({
  content: '# Hello FreeNote\n\n开始输入 Markdown 内容…',
  isDirty: false,
})

export function setDocumentContent(content: string) {
  documentStore.content = content
  documentStore.isDirty = true
}

export function replaceDocumentContent(content: string) {
  documentStore.content = content
  documentStore.isDirty = false
}
