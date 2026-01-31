<template>
  <div ref="editorRoot" class="cm-editor-root"></div>
</template>

<script setup lang="ts">
import { watch } from 'vue'
import { onMounted, onBeforeUnmount, ref } from 'vue'
import { EditorView } from '@codemirror/view'
import { EditorState } from '@codemirror/state'
import { markdown } from '@codemirror/lang-markdown'
import { Decoration, ViewPlugin, ViewUpdate } from '@codemirror/view'

const editorRoot = ref<HTMLDivElement | null>(null)
let view: EditorView | null = null

const props = defineProps<{
  modelValue: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()
const markdownWeakener = ViewPlugin.fromClass(
  class {
    decorations: Decoration.Set

    constructor(view: EditorView) {
      this.decorations = this.buildDecorations(view)
    }

    update(update: ViewUpdate) {
      if (
        update.docChanged ||
        update.selectionSet ||
        update.viewportChanged
      ) {
        this.decorations = this.buildDecorations(update.view)
      }
    }

    buildDecorations(view: EditorView) {
      const builder: Decoration[] = []
      const { state } = view
      const cursorLine = state.doc.lineAt(
        state.selection.main.head
      ).number

      for (const { from, to } of view.visibleRanges) {
        let pos = from
        while (pos <= to) {
          const line = state.doc.lineAt(pos)

          // 光标所在行不弱化
          if (line.number !== cursorLine) {
            const regex = /(^#{1,6}\s)|(\*\*|\*|__|_)/g
            let match

            while ((match = regex.exec(line.text))) {
              const start = line.from + match.index
              const end = start + match[0].length

              builder.push(
                Decoration.mark({
                  class: 'md-weak',
                }).range(start, end)
              )
            }
          }

          pos = line.to + 1
        }
      }

      return Decoration.set(builder)
    }
  },
  {
    decorations: v => v.decorations,
  }
)


onMounted(() => {
  if (!editorRoot.value) return

  const state = EditorState.create({
    doc: props.modelValue,
    extensions: [
        markdownWeakener,
        markdown(),
        EditorView.updateListener.of(update => {
            if (update.docChanged) {
                const content = update.state.doc.toString()
                emit('update:modelValue', content)
            }   
        }),

    ],
  })

  view = new EditorView({
    state,
    parent: editorRoot.value,
  })
})

watch(
  () => props.modelValue,
  (newValue) => {
    if (!view) return

    const current = view.state.doc.toString()
    if (newValue !== current) {
      view.dispatch({
        changes: {
          from: 0,
          to: current.length,
          insert: newValue,
        },
      })
    }
  }
)


onBeforeUnmount(() => {
  view?.destroy()
  view = null
})
</script>

<style scoped>
.cm-editor-root {
  height: 100%;
}
:deep(.md-weak) {
  opacity: 0.3;
  transition: opacity 0.15s;
}
/* 正文排版 */
:deep(.cm-content) {
  font-size: 15.5px;
  line-height: 1.8;
  padding: 10px 6px;
  font-family:
    Inter,
    system-ui,
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    Helvetica,
    Arial,
    sans-serif;
  letter-spacing: 0.01em;
}


/* 段落之间留白 */
:deep(.cm-line) {
  padding: 2px 0;
}

/* 标题层级（CodeMirror Markdown token class） */
:deep(.cm-header.cm-header-1) {
  font-size: 1.8em;
  font-weight: 600;
  margin: 0.6em 0 0.4em;
}

:deep(.cm-header.cm-header-2) {
  font-size: 1.5em;
  font-weight: 600;
  margin: 0.5em 0 0.3em;
}

:deep(.cm-header.cm-header-3) {
  font-size: 1.25em;
  font-weight: 600;
  margin: 0.4em 0 0.2em;
}

/* 引用 */
:deep(.cm-quote) {
  color: #555;
  padding-left: 12px;
  border-left: 3px solid #ddd;
}

/* 行内代码 */
:deep(.cm-inline-code) {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  background: #f5f5f5;
  padding: 2px 4px;
  border-radius: 4px;
  font-size: 0.9em;
}

/* 代码块（先做最轻样式） */
:deep(.cm-codeblock) {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  background: #fafafa;
  padding: 8px;
  border-radius: 6px;
  font-size: 0.9em;
}
/* 去除 CodeMirror 获取焦点时的虚线框 */
:deep(.cm-editor.cm-focused) {
  outline: none;
}

/* 有些主题/版本会在 scroller 上画边框，一并去掉 */
:deep(.cm-scroller) {
  outline: none;
}


</style>
