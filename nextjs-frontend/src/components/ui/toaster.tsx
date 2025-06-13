"use client"

import {
  Toast,
  ToastClose,
  ToastDescription,
  ToastProvider,
  ToastTitle,
  ToastViewport,
} from "./toast"
import { useToast } from "./use-toast"

export function Toaster() {
  const { toasts } = useToast()

  return (
    <ToastProvider>
      {toasts.map(function ({ id, title, description, action, ...props }) {
        return (
          <Toast key={id} {...props} className="group border-2 shadow-lg">
            <div className="grid gap-2">
              {title && <ToastTitle className="text-base font-semibold">{title}</ToastTitle>}
              {description && (
                <ToastDescription className="text-sm opacity-90">{description}</ToastDescription>
              )}
            </div>
            {action}
            <ToastClose className="opacity-70 transition-opacity hover:opacity-100" />
          </Toast>
        )
      })}
      <ToastViewport className="p-6 gap-2" />
    </ToastProvider>
  )
}

export { useToast } from "./use-toast"
export { ToastProvider, ToastViewport } from "./toast"