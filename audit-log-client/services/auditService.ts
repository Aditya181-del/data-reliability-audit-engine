import { AuditResponse, ApiErrorDetail } from '../types';

const API_URL = 'http://localhost:8000/audit';

/**
 * Validates whether a server response satisfies the minimum
 * guaranteed backend contract.
 *
 * Backend guarantees:
 * - decision (string)
 * - audit (object)
 *
 * Explanation is OPTIONAL by design and must NOT be required here.
 */
function isAuditResponse(data: any): data is AuditResponse {
  return (
    typeof data === 'object' &&
    data !== null &&
    typeof data.decision === 'string' &&
    typeof data.audit === 'object'
  );
}

/**
 * Submits an audit request to the backend.
 *
 * This function is a pure transport + validation layer.
 * It does NOT interpret results or make decisions.
 */
export function submitAuditRequest(
  dataset: File,
  audience: string,
  metadata?: File,
  onProgress?: (percentage: number) => void
): Promise<AuditResponse> {
  return new Promise((resolve, reject) => {
    const formData = new FormData();
    formData.append('dataset', dataset);
    formData.append('audience', audience);

    if (metadata) {
      formData.append('metadata', metadata);
    }

    const xhr = new XMLHttpRequest();
    xhr.open('POST', API_URL);

    // Optional upload progress reporting
    if (onProgress) {
      xhr.upload.onprogress = (event) => {
        if (event.lengthComputable) {
          const percentComplete = (event.loaded / event.total) * 100;
          onProgress(percentComplete);
        }
      };
    }

    xhr.onload = () => {
      const textBody = xhr.responseText;

      // Success responses
      if (xhr.status >= 200 && xhr.status < 300) {
        try {
          const json = JSON.parse(textBody);

          if (!isAuditResponse(json)) {
            const errorDetail: ApiErrorDetail = {
              message:
                'Server response does not match expected audit contract.',
              status: xhr.status,
              rawResponse: textBody,
              type: 'validation',
            };
            reject(errorDetail);
            return;
          }

          resolve(json);
        } catch {
          const errorDetail: ApiErrorDetail = {
            message: 'Server response was not valid JSON.',
            status: xhr.status,
            rawResponse: textBody,
            type: 'parse',
          };
          reject(errorDetail);
        }
      } else {
        // Server returned an error status
        const errorDetail: ApiErrorDetail = {
          message: `Server returned error status ${xhr.status}.`,
          status: xhr.status,
          rawResponse: textBody,
          type: 'server',
        };
        reject(errorDetail);
      }
    };

    xhr.onerror = () => {
      const errorDetail: ApiErrorDetail = {
        message:
          'Network request failed. Backend may be unreachable.',
        type: 'network',
      };
      reject(errorDetail);
    };

    xhr.send(formData);
  });
}