/**
 * Simple logger utility for application monitoring.
 * Logs structured error objects for easier debugging.
 */
export function logError(error, context = 'Unknown Context') {
  console.error({
    context,
    message: error.message || error,
    stack: error.stack || null,
    time: new Date().toISOString()
  })
}

export function logInfo(message, context = 'System') {
  console.info({
    context,
    message,
    time: new Date().toISOString()
  })
}
