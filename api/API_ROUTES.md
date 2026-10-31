# Dify API Routes

> Auto-extracted from `api/controllers/` source code.
> Generated: 2026-05-02

---

## Overview

| API | Base Prefix | Auth | Routes |
|-----|-------------|------|--------|
| [Console API](#console-api) | `/console/api` | Session (Cookie) | 339 |
| [Service API](#service-api) | `/v1` | `Authorization: Bearer <api-key>` | 64 |

---

## Console API

> Base prefix: `/console/api`  
> Auth: Login session required (`@login_required`)

### Authentication

| Method | Path | File |
|--------|------|------|
| `POST` | `/login` | `auth/login.py` |
| `POST` | `/logout` | `auth/login.py` |
| `POST` | `/refresh-token` | `auth/login.py` |
| `POST` | `/reset-password` | `auth/login.py` |
| `POST` | `/forgot-password` | `auth/forgot_password.py` |
| `POST` | `/forgot-password/resets` | `auth/forgot_password.py` |
| `POST` | `/forgot-password/validity` | `auth/forgot_password.py` |
| `POST` | `/activate` | `auth/activate.py` |
| `GET` | `/activate/check` | `auth/activate.py` |
| `POST` | `/email-code-login` | `auth/login.py` |
| `POST` | `/email-code-login/validity` | `auth/login.py` |
| `POST` | `/email-register` | `auth/email_register.py` |
| `POST` | `/email-register/send-email` | `auth/email_register.py` |
| `POST` | `/email-register/validity` | `auth/email_register.py` |

### OAuth

| Method | Path | File |
|--------|------|------|
| `GET` | `/oauth/authorize/<provider>` | `auth/oauth.py` |
| `GET` | `/oauth/login/<provider>` | `auth/oauth.py` |
| `POST` | `/oauth/provider` | `auth/oauth_server.py` |
| `POST` | `/oauth/provider/account` | `auth/oauth_server.py` |
| `POST` | `/oauth/provider/authorize` | `auth/oauth_server.py` |
| `POST` | `/oauth/provider/token` | `auth/oauth_server.py` |
| `GET` | `/oauth/data-source/<provider>` | `auth/data_source_oauth.py` |
| `GET` | `/oauth/data-source/binding/<provider>` | `auth/data_source_oauth.py` |
| `GET` | `/oauth/data-source/callback/<provider>` | `auth/data_source_oauth.py` |
| `GET` | `/oauth/data-source/<provider>/<binding_id>/sync` | `auth/data_source_oauth.py` |
| `GET` | `/oauth/plugin/<provider>/tool/authorization-url` | `workspace/tool_providers.py` |
| `GET` | `/oauth/plugin/<provider>/tool/callback` | `workspace/tool_providers.py` |
| `GET` | `/oauth/plugin/<provider>/trigger/callback` | `workspace/trigger_providers.py` |
| `GET` | `/oauth/plugin/<provider_id>/datasource/callback` | `datasets/rag_pipeline/datasource_auth.py` |
| `GET` | `/oauth/plugin/<provider_id>/datasource/get-authorization-url` | `datasets/rag_pipeline/datasource_auth.py` |
| `GET` | `/mcp/oauth/callback` | `workspace/tool_providers.py` |

### Account

| Method | Path | File |
|--------|------|------|
| `GET` | `/account/profile` | `workspace/account.py` |
| `POST` | `/account/name` | `workspace/account.py` |
| `GET,POST` | `/account/avatar` | `workspace/account.py` |
| `POST` | `/account/interface-language` | `workspace/account.py` |
| `POST` | `/account/interface-theme` | `workspace/account.py` |
| `POST` | `/account/timezone` | `workspace/account.py` |
| `POST` | `/account/password` | `workspace/account.py` |
| `POST` | `/account/init` | `workspace/account.py` |
| `GET` | `/account/integrates` | `workspace/account.py` |
| `POST` | `/account/change-email` | `workspace/account.py` |
| `POST` | `/account/change-email/check-email-unique` | `workspace/account.py` |
| `POST` | `/account/change-email/reset` | `workspace/account.py` |
| `POST` | `/account/change-email/validity` | `workspace/account.py` |
| `POST` | `/account/delete` | `workspace/account.py` |
| `POST` | `/account/delete/feedback` | `workspace/account.py` |
| `GET` | `/account/delete/verify` | `workspace/account.py` |
| `GET,POST` | `/account/education` | `workspace/account.py` |
| `GET` | `/account/education/autocomplete` | `workspace/account.py` |
| `GET` | `/account/education/verify` | `workspace/account.py` |

### Apps

| Method | Path | File |
|--------|------|------|
| `GET` | `/apps` | `app/app.py` |
| `GET` | `/apps/<app_id>` | `app/app.py` |
| `POST` | `/apps/<app_id>/copy` | `app/app.py` |
| `GET` | `/apps/<app_id>/export` | `app/app.py` |
| `POST` | `/apps/<app_id>/icon` | `app/app.py` |
| `POST` | `/apps/<app_id>/name` | `app/app.py` |
| `POST` | `/apps/<app_id>/site-enable` | `app/app.py` |
| `POST` | `/apps/<app_id>/api-enable` | `app/app.py` |
| `POST` | `/apps/<app_id>/trigger-enable` | `app/workflow_trigger.py` |
| `GET` | `/apps/<app_id>/triggers` | `app/workflow_trigger.py` |
| `POST` | `/apps/<app_id>/publish-to-creators-platform` | `app/app.py` |
| `GET,POST` | `/apps/<app_id>/trace` | `app/app.py` |
| `GET` | `/apps/<app_id>/trace-config` | `app/ops_trace.py` |
| `POST` | `/apps/<app_id>/convert-to-workflow` | `app/workflow.py` |
| `POST` | `/apps/<app_id>/model-config` | `app/model_config.py` |
| `POST` | `/apps/<app_id>/site` | `app/site.py` |
| `POST` | `/apps/<app_id>/site/access-token-reset` | `app/site.py` |
| `GET` | `/apps/<app_id>/server` | `app/mcp_server.py` |
| `GET` | `/apps/<server_id>/server/refresh` | `app/mcp_server.py` |
| `GET,POST` | `/apps/<resource_id>/api-keys` | `apikey.py` |
| `DELETE` | `/apps/<resource_id>/api-keys/<api_key_id>` | `apikey.py` |
| `POST` | `/apps/imports` | `app/app_import.py` |
| `GET` | `/apps/imports/<app_id>/check-dependencies` | `app/app_import.py` |
| `POST` | `/apps/imports/<import_id>/confirm` | `app/app_import.py` |

### Apps — Workflow

| Method | Path | File |
|--------|------|------|
| `GET,POST` | `/apps/<app_id>/workflows/draft` | `app/workflow.py` |
| `GET` | `/apps/<app_id>/workflows/draft/conversation-variables` | `app/workflow_draft_variable.py` |
| `GET` | `/apps/<app_id>/workflows/draft/environment-variables` | `app/workflow_draft_variable.py` |
| `POST` | `/apps/<app_id>/workflows/draft/features` | `app/workflow.py` |
| `GET` | `/apps/<app_id>/workflows/draft/variables` | `app/workflow_draft_variable.py` |
| `GET` | `/apps/<app_id>/workflows/draft/variables/<variable_id>` | `app/workflow_draft_variable.py` |
| `PUT` | `/apps/<app_id>/workflows/draft/variables/<variable_id>/reset` | `app/workflow_draft_variable.py` |
| `GET` | `/apps/<app_id>/workflows/draft/system-variables` | `app/workflow_draft_variable.py` |
| `GET,DELETE` | `/apps/<app_id>/workflows/draft/nodes/<node_id>/variables` | `app/workflow_draft_variable.py` |
| `POST` | `/apps/<app_id>/workflows/draft/run` | `app/workflow.py` |
| `POST` | `/apps/<app_id>/workflows/draft/nodes/<node_id>/run` | `app/workflow.py` |
| `POST` | `/apps/<app_id>/workflows/draft/nodes/<node_id>/trigger/run` | `app/workflow.py` |
| `GET` | `/apps/<app_id>/workflows/draft/nodes/<node_id>/last-run` | `app/workflow.py` |
| `POST` | `/apps/<app_id>/workflows/draft/iteration/nodes/<node_id>/run` | `app/workflow.py` |
| `POST` | `/apps/<app_id>/workflows/draft/loop/nodes/<node_id>/run` | `app/workflow.py` |
| `POST` | `/apps/<app_id>/workflows/draft/trigger/run` | `app/workflow.py` |
| `POST` | `/apps/<app_id>/workflows/draft/trigger/run-all` | `app/workflow.py` |
| `POST` | `/apps/<app_id>/workflows/draft/human-input/nodes/<node_id>/form/preview` | `app/workflow.py` |
| `POST` | `/apps/<app_id>/workflows/draft/human-input/nodes/<node_id>/form/run` | `app/workflow.py` |
| `POST` | `/apps/<app_id>/workflows/draft/human-input/nodes/<node_id>/delivery-test` | `app/workflow.py` |
| `GET` | `/apps/<app_id>/workflows/publish` | `app/workflow.py` |
| `POST` | `/apps/<app_id>/workflows/publish` | `app/workflow.py` |
| `GET` | `/apps/<app_id>/workflows` | `app/workflow.py` |
| `PATCH` | `/apps/<app_id>/workflows/<workflow_id>` | `app/workflow.py` |
| `POST` | `/apps/<app_id>/workflows/<workflow_id>/restore` | `app/workflow.py` |
| `GET` | `/apps/<app_id>/workflows/default-workflow-block-configs` | `app/workflow.py` |
| `GET` | `/apps/<app_id>/workflows/default-workflow-block-configs/<block_type>` | `app/workflow.py` |
| `GET` | `/apps/<app_id>/workflows/triggers/webhook` | `app/workflow_trigger.py` |
| `POST` | `/apps/<app_id>/workflow-runs/tasks/<task_id>/stop` | `app/workflow.py` |
| `GET` | `/apps/workflows/online-users` | `app/workflow.py` |

### Apps — Advanced Chat

| Method | Path | File |
|--------|------|------|
| `POST` | `/apps/<app_id>/advanced-chat/workflows/draft/run` | `app/workflow.py` |
| `POST` | `/apps/<app_id>/advanced-chat/workflows/draft/iteration/nodes/<node_id>/run` | `app/workflow.py` |
| `POST` | `/apps/<app_id>/advanced-chat/workflows/draft/loop/nodes/<node_id>/run` | `app/workflow.py` |
| `POST` | `/apps/<app_id>/advanced-chat/workflows/draft/human-input/nodes/<node_id>/form/preview` | `app/workflow.py` |
| `POST` | `/apps/<app_id>/advanced-chat/workflows/draft/human-input/nodes/<node_id>/form/run` | `app/workflow.py` |
| `GET` | `/apps/<app_id>/advanced-chat/workflow-runs` | `app/workflow_run.py` |
| `GET` | `/apps/<app_id>/advanced-chat/workflow-runs/count` | `app/workflow_run.py` |

### Apps — Chat & Completion

| Method | Path | File |
|--------|------|------|
| `POST` | `/apps/<app_id>/chat-messages` | `app/completion.py` |
| `GET` | `/apps/<app_id>/chat-messages` | `app/message.py` |
| `POST` | `/apps/<app_id>/chat-messages/<task_id>/stop` | `app/completion.py` |
| `GET` | `/apps/<app_id>/chat-messages/<message_id>/suggested-questions` | `app/message.py` |
| `GET` | `/apps/<app_id>/chat-conversations` | `app/conversation.py` |
| `GET` | `/apps/<app_id>/chat-conversations/<conversation_id>` | `app/conversation.py` |
| `POST` | `/apps/<app_id>/completion-messages` | `app/completion.py` |
| `POST` | `/apps/<app_id>/completion-messages/<task_id>/stop` | `app/completion.py` |
| `GET` | `/apps/<app_id>/completion-conversations` | `app/conversation.py` |
| `GET` | `/apps/<app_id>/completion-conversations/<conversation_id>` | `app/conversation.py` |
| `GET` | `/apps/<app_id>/conversation-variables` | `app/conversation_variables.py` |

### Apps — Messages & Feedbacks

| Method | Path | File |
|--------|------|------|
| `GET` | `/apps/<app_id>/messages/<message_id>` | `app/message.py` |
| `POST` | `/apps/<app_id>/feedbacks` | `app/message.py` |
| `GET` | `/apps/<app_id>/feedbacks/export` | `app/message.py` |
| `GET` | `/apps/<app_id>/annotations/count` | `app/message.py` |

### Apps — Annotations

| Method | Path | File |
|--------|------|------|
| `GET` | `/apps/<app_id>/annotations` | `app/annotation.py` |
| `POST` | `/apps/<app_id>/annotations/<annotation_id>` | `app/annotation.py` |
| `GET` | `/apps/<app_id>/annotations/<annotation_id>/hit-histories` | `app/annotation.py` |
| `GET` | `/apps/<app_id>/annotations/count` | `app/message.py` |
| `GET` | `/apps/<app_id>/annotations/export` | `app/annotation.py` |
| `POST` | `/apps/<app_id>/annotations/batch-import` | `app/annotation.py` |
| `GET` | `/apps/<app_id>/annotations/batch-import-status/<job_id>` | `app/annotation.py` |
| `GET` | `/apps/<app_id>/annotation-setting` | `app/annotation.py` |
| `POST` | `/apps/<app_id>/annotation-settings/<annotation_setting_id>` | `app/annotation.py` |
| `POST` | `/apps/<app_id>/annotation-reply/<action>` | `app/annotation.py` |
| `GET` | `/apps/<app_id>/annotation-reply/<action>/status/<job_id>` | `app/annotation.py` |

### Apps — Workflow Comments

| Method | Path | File |
|--------|------|------|
| `GET` | `/apps/<app_id>/workflow/comments` | `app/workflow_comment.py` |
| `POST` | `/apps/<app_id>/workflow/comments` | `app/workflow_comment.py` |
| `GET` | `/apps/<app_id>/workflow/comments/<comment_id>` | `app/workflow_comment.py` |
| `PATCH` | `/apps/<app_id>/workflow/comments/<comment_id>` | `app/workflow_comment.py` |
| `DELETE` | `/apps/<app_id>/workflow/comments/<comment_id>` | `app/workflow_comment.py` |
| `POST` | `/apps/<app_id>/workflow/comments/<comment_id>/replies` | `app/workflow_comment.py` |
| `PUT` | `/apps/<app_id>/workflow/comments/<comment_id>/replies/<reply_id>` | `app/workflow_comment.py` |
| `POST` | `/apps/<app_id>/workflow/comments/<comment_id>/resolve` | `app/workflow_comment.py` |
| `GET` | `/apps/<app_id>/workflow/comments/mention-users` | `app/workflow_comment.py` |

### Apps — Runs & Logs

| Method | Path | File |
|--------|------|------|
| `GET` | `/apps/<app_id>/workflow-runs` | `app/workflow_run.py` |
| `GET` | `/apps/<app_id>/workflow-runs/<run_id>` | `app/workflow_run.py` |
| `GET` | `/apps/<app_id>/workflow-runs/<run_id>/export` | `app/workflow_run.py` |
| `GET` | `/apps/<app_id>/workflow-runs/<run_id>/node-executions` | `app/workflow_run.py` |
| `GET` | `/apps/<app_id>/workflow-runs/count` | `app/workflow_run.py` |
| `GET` | `/apps/<app_id>/workflow/<workflow_run_id>/pause-details` | `app/workflow_run.py` |
| `GET` | `/apps/<app_id>/workflow-app-logs` | `app/workflow_app_log.py` |
| `GET` | `/apps/<app_id>/workflow-archived-logs` | `app/workflow_app_log.py` |
| `GET` | `/apps/<app_id>/agent/logs` | `app/agent.py` |
| `GET` | `/workflow/<workflow_run_id>/events` | `human_input_form.py` |
| `GET` | `/workflow/<workflow_run_id>/pause-details` | `app/workflow_run.py` |

### Apps — Statistics

| Method | Path | File |
|--------|------|------|
| `GET` | `/apps/<app_id>/statistics/daily-messages` | `app/statistic.py` |
| `GET` | `/apps/<app_id>/statistics/daily-conversations` | `app/statistic.py` |
| `GET` | `/apps/<app_id>/statistics/daily-end-users` | `app/statistic.py` |
| `GET` | `/apps/<app_id>/statistics/average-response-time` | `app/statistic.py` |
| `GET` | `/apps/<app_id>/statistics/average-session-interactions` | `app/statistic.py` |
| `GET` | `/apps/<app_id>/statistics/user-satisfaction-rate` | `app/statistic.py` |
| `GET` | `/apps/<app_id>/statistics/token-costs` | `app/statistic.py` |
| `GET` | `/apps/<app_id>/statistics/tokens-per-second` | `app/statistic.py` |
| `GET` | `/apps/<app_id>/workflow/statistics/daily-conversations` | `app/workflow_statistic.py` |
| `GET` | `/apps/<app_id>/workflow/statistics/daily-terminals` | `app/workflow_statistic.py` |
| `GET` | `/apps/<app_id>/workflow/statistics/average-app-interactions` | `app/workflow_statistic.py` |
| `GET` | `/apps/<app_id>/workflow/statistics/token-costs` | `app/workflow_statistic.py` |

### Apps — Audio & Media

| Method | Path | File |
|--------|------|------|
| `POST` | `/apps/<app_id>/audio-to-text` | `app/audio.py` |
| `POST` | `/apps/<app_id>/text-to-audio` | `app/audio.py` |
| `GET` | `/apps/<app_id>/text-to-audio/voices` | `app/audio.py` |

### Datasets (Knowledge Base)

| Method | Path | File |
|--------|------|------|
| `GET` | `/datasets` | `datasets/datasets.py` |
| `POST` | `/datasets/init` | `datasets/datasets_document.py` |
| `GET` | `/datasets/indexing-estimate` | `datasets/datasets.py` |
| `GET` | `/datasets/process-rule` | `datasets/datasets_document.py` |
| `GET` | `/datasets/retrieval-setting` | `datasets/datasets.py` |
| `GET` | `/datasets/retrieval-setting/<vector_type>` | `datasets/datasets.py` |
| `GET` | `/datasets/api-base-info` | `datasets/datasets.py` |
| `GET,POST` | `/datasets/api-keys` | `datasets/datasets.py` |
| `DELETE` | `/datasets/api-keys/<api_key_id>` | `datasets/datasets.py` |
| `GET` | `/datasets/metadata/built-in` | `datasets/metadata.py` |
| `POST` | `/datasets/external` | `datasets/external.py` |
| `GET` | `/datasets/external-knowledge-api` | `datasets/external.py` |
| `GET,PATCH` | `/datasets/external-knowledge-api/<external_knowledge_api_id>` | `datasets/external.py` |
| `GET` | `/datasets/external-knowledge-api/<external_knowledge_api_id>/use-check` | `datasets/external.py` |
| `GET` | `/datasets/<dataset_id>` | `datasets/datasets.py` |
| `POST` | `/datasets/<dataset_id>/api-keys/<status>` | `datasets/datasets.py` |
| `GET` | `/datasets/<dataset_id>/auto-disable-logs` | `datasets/datasets.py` |
| `GET` | `/datasets/<dataset_id>/use-check` | `datasets/datasets.py` |
| `GET` | `/datasets/<dataset_id>/related-apps` | `datasets/datasets.py` |
| `GET` | `/datasets/<dataset_id>/queries` | `datasets/datasets.py` |
| `GET` | `/datasets/<dataset_id>/indexing-status` | `datasets/datasets.py` |
| `GET` | `/datasets/<dataset_id>/error-docs` | `datasets/datasets.py` |
| `GET` | `/datasets/<dataset_id>/permission-part-users` | `datasets/datasets.py` |
| `GET,POST` | `/datasets/<resource_id>/api-keys` | `apikey.py` |
| `DELETE` | `/datasets/<resource_id>/api-keys/<api_key_id>` | `apikey.py` |

### Datasets — Documents

| Method | Path | File |
|--------|------|------|
| `GET,POST` | `/datasets/<dataset_id>/documents` | `datasets/datasets_document.py` |
| `GET` | `/datasets/<dataset_id>/documents/<document_id>` | `datasets/datasets_document.py` |
| `DELETE` | `/datasets/<dataset_id>/documents/<document_id>` | `datasets/datasets_document.py` |
| `GET` | `/datasets/<dataset_id>/documents/<document_id>/download` | `datasets/datasets_document.py` |
| `GET` | `/datasets/<dataset_id>/documents/<document_id>/indexing-status` | `datasets/datasets_document.py` |
| `GET` | `/datasets/<dataset_id>/documents/<document_id>/indexing-estimate` | `datasets/datasets_document.py` |
| `GET` | `/datasets/<dataset_id>/documents/<document_id>/pipeline-execution-log` | `datasets/datasets_document.py` |
| `GET` | `/datasets/<dataset_id>/documents/<document_id>/summary-status` | `datasets/datasets_document.py` |
| `GET` | `/datasets/<dataset_id>/documents/<document_id>/website-sync` | `datasets/datasets_document.py` |
| `PUT` | `/datasets/<dataset_id>/documents/<document_id>/metadata` | `datasets/datasets_document.py` |
| `POST` | `/datasets/<dataset_id>/documents/<document_id>/rename` | `datasets/datasets_document.py` |
| `PATCH` | `/datasets/<dataset_id>/documents/<document_id>/processing/<action>` | `datasets/datasets_document.py` |
| `PATCH` | `/datasets/<dataset_id>/documents/<document_id>/processing/pause` | `datasets/datasets_document.py` |
| `PATCH` | `/datasets/<dataset_id>/documents/<document_id>/processing/resume` | `datasets/datasets_document.py` |
| `GET` | `/datasets/<dataset_id>/documents/<document_id>/notion/sync` | `datasets/data_source.py` |
| `GET` | `/datasets/<dataset_id>/documents/<document_id>/segments` | `datasets/datasets_segments.py` |
| `POST` | `/datasets/<dataset_id>/documents/<document_id>/segment` | `datasets/datasets_segments.py` |
| `PATCH` | `/datasets/<dataset_id>/documents/<document_id>/segment/<action>` | `datasets/datasets_segments.py` |
| `PATCH` | `/datasets/<dataset_id>/documents/<document_id>/segments/<segment_id>` | `datasets/datasets_segments.py` |
| `POST` | `/datasets/<dataset_id>/documents/<document_id>/segments/<segment_id>/child_chunks` | `datasets/datasets_segments.py` |
| `POST` | `/datasets/<dataset_id>/documents/download-zip` | `datasets/datasets_document.py` |
| `POST` | `/datasets/<dataset_id>/documents/generate-summary` | `datasets/datasets_document.py` |
| `POST` | `/datasets/<dataset_id>/documents/metadata` | `datasets/metadata.py` |
| `PATCH` | `/datasets/<dataset_id>/documents/status/<action>/batch` | `datasets/datasets_document.py` |
| `GET` | `/datasets/<dataset_id>/batch/<batch>/indexing-status` | `datasets/datasets_document.py` |
| `GET` | `/datasets/<dataset_id>/batch/<batch>/indexing-estimate` | `datasets/datasets_document.py` |
| `POST` | `/datasets/<dataset_id>/retry` | `datasets/datasets_document.py` |

### Datasets — Metadata & Hit Testing

| Method | Path | File |
|--------|------|------|
| `GET,POST` | `/datasets/<dataset_id>/metadata` | `datasets/metadata.py` |
| `PATCH,DELETE` | `/datasets/<dataset_id>/metadata/<metadata_id>` | `datasets/metadata.py` |
| `POST` | `/datasets/<dataset_id>/metadata/built-in/<action>` | `datasets/metadata.py` |
| `POST` | `/datasets/<dataset_id>/hit-testing` | `datasets/hit_testing.py` |
| `POST` | `/datasets/<dataset_id>/external-hit-testing` | `datasets/external.py` |
| `POST` | `/test/retrieval` | `datasets/external.py` |

### Datasets — Notion & Website

| Method | Path | File |
|--------|------|------|
| `GET` | `/notion/pre-import/pages` | `datasets/data_source.py` |
| `GET` | `/datasets/<dataset_id>/notion/sync` | `datasets/data_source.py` |
| `POST` | `/website/crawl` | `datasets/website.py` |
| `GET` | `/website/crawl/status/<job_id>` | `datasets/website.py` |

### RAG Pipelines

| Method | Path | File |
|--------|------|------|
| `GET` | `/rag/pipeline/templates` | `datasets/rag_pipeline/rag_pipeline.py` |
| `GET` | `/rag/pipeline/templates/<template_id>` | `datasets/rag_pipeline/rag_pipeline.py` |
| `GET,PATCH,DELETE` | `/rag/pipeline/customized/templates/<template_id>` | `datasets/rag_pipeline/rag_pipeline.py` |
| `POST` | `/rag/pipelines/<pipeline_id>/customized/publish` | `datasets/rag_pipeline/rag_pipeline.py` |
| `POST` | `/rag/pipeline/dataset` | `datasets/rag_pipeline/rag_pipeline_datasets.py` |
| `POST` | `/rag/pipeline/empty-dataset` | `datasets/rag_pipeline/rag_pipeline_datasets.py` |
| `GET` | `/rag/pipelines/<pipeline_id>/exports` | `datasets/rag_pipeline/rag_pipeline_import.py` |
| `POST` | `/rag/pipelines/imports` | `datasets/rag_pipeline/rag_pipeline_import.py` |
| `GET` | `/rag/pipelines/imports/<pipeline_id>/check-dependencies` | `datasets/rag_pipeline/rag_pipeline_import.py` |
| `POST` | `/rag/pipelines/imports/<import_id>/confirm` | `datasets/rag_pipeline/rag_pipeline_import.py` |
| `POST` | `/rag/pipelines/transform/datasets/<dataset_id>` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `GET` | `/rag/pipelines/datasource-plugins` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `GET` | `/rag/pipelines/recommended-plugins` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `GET` | `/rag/pipelines/<pipeline_id>/workflows` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `GET,POST` | `/rag/pipelines/<pipeline_id>/workflows/draft` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `GET` | `/rag/pipelines/<pipeline_id>/workflows/draft/environment-variables` | `datasets/rag_pipeline/rag_pipeline_draft_variable.py` |
| `GET` | `/rag/pipelines/<pipeline_id>/workflows/draft/system-variables` | `datasets/rag_pipeline/rag_pipeline_draft_variable.py` |
| `GET` | `/rag/pipelines/<pipeline_id>/workflows/draft/variables` | `datasets/rag_pipeline/rag_pipeline_draft_variable.py` |
| `GET,PATCH` | `/rag/pipelines/<pipeline_id>/workflows/draft/variables/<variable_id>` | `datasets/rag_pipeline/rag_pipeline_draft_variable.py` |
| `PUT` | `/rag/pipelines/<pipeline_id>/workflows/draft/variables/<variable_id>/reset` | `datasets/rag_pipeline/rag_pipeline_draft_variable.py` |
| `GET,DELETE` | `/rag/pipelines/<pipeline_id>/workflows/draft/nodes/<node_id>/variables` | `datasets/rag_pipeline/rag_pipeline_draft_variable.py` |
| `POST` | `/rag/pipelines/<pipeline_id>/workflows/draft/run` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `POST` | `/rag/pipelines/<pipeline_id>/workflows/draft/nodes/<node_id>/run` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `GET` | `/rag/pipelines/<pipeline_id>/workflows/draft/nodes/<node_id>/last-run` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `POST` | `/rag/pipelines/<pipeline_id>/workflows/draft/iteration/nodes/<node_id>/run` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `POST` | `/rag/pipelines/<pipeline_id>/workflows/draft/loop/nodes/<node_id>/run` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `POST` | `/rag/pipelines/<pipeline_id>/workflows/draft/datasource/nodes/<node_id>/run` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `POST` | `/rag/pipelines/<pipeline_id>/workflows/draft/datasource/variables-inspect` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `GET` | `/rag/pipelines/<pipeline_id>/workflows/draft/pre-processing/parameters` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `GET` | `/rag/pipelines/<pipeline_id>/workflows/draft/processing/parameters` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `GET,POST` | `/rag/pipelines/<pipeline_id>/workflows/publish` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `POST` | `/rag/pipelines/<pipeline_id>/workflows/published/run` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `POST` | `/rag/pipelines/<pipeline_id>/workflows/published/datasource/nodes/<node_id>/run` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `POST` | `/rag/pipelines/<pipeline_id>/workflows/published/datasource/nodes/<node_id>/preview` | `datasets/rag_pipeline/datasource_content_preview.py` |
| `GET` | `/rag/pipelines/<pipeline_id>/workflows/published/pre-processing/parameters` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `GET` | `/rag/pipelines/<pipeline_id>/workflows/published/processing/parameters` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `PATCH` | `/rag/pipelines/<pipeline_id>/workflows/<workflow_id>` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `POST` | `/rag/pipelines/<pipeline_id>/workflows/<workflow_id>/restore` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `GET` | `/rag/pipelines/<pipeline_id>/workflows/default-workflow-block-configs` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `GET` | `/rag/pipelines/<pipeline_id>/workflows/default-workflow-block-configs/<block_type>` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `GET` | `/rag/pipelines/<pipeline_id>/workflow-runs` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `GET` | `/rag/pipelines/<pipeline_id>/workflow-runs/<run_id>` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `GET` | `/rag/pipelines/<pipeline_id>/workflow-runs/<run_id>/node-executions` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |
| `POST` | `/rag/pipelines/<pipeline_id>/workflow-runs/tasks/<task_id>/stop` | `datasets/rag_pipeline/rag_pipeline_workflow.py` |

### Datasource Auth (RAG)

| Method | Path | File |
|--------|------|------|
| `GET,POST` | `/auth/plugin/datasource/<provider_id>` | `datasets/rag_pipeline/datasource_auth.py` |
| `POST,DELETE` | `/auth/plugin/datasource/<provider_id>/custom-client` | `datasets/rag_pipeline/datasource_auth.py` |
| `POST` | `/auth/plugin/datasource/<provider_id>/default` | `datasets/rag_pipeline/datasource_auth.py` |
| `POST` | `/auth/plugin/datasource/<provider_id>/delete` | `datasets/rag_pipeline/datasource_auth.py` |
| `POST` | `/auth/plugin/datasource/<provider_id>/update` | `datasets/rag_pipeline/datasource_auth.py` |
| `POST` | `/auth/plugin/datasource/<provider_id>/update-name` | `datasets/rag_pipeline/datasource_auth.py` |
| `GET` | `/auth/plugin/datasource/default-list` | `datasets/rag_pipeline/datasource_auth.py` |
| `GET` | `/auth/plugin/datasource/list` | `datasets/rag_pipeline/datasource_auth.py` |

### Workspaces

| Method | Path | File |
|--------|------|------|
| `GET` | `/workspaces` | `workspace/workspace.py` |
| `GET` | `/workspaces/current` | `workspace/workspace.py` |
| `GET` | `/workspaces/info` | `workspace/workspace.py` |
| `POST` | `/workspaces/switch` | `workspace/workspace.py` |
| `POST` | `/workspaces/custom-config` | `workspace/workspace.py` |
| `POST` | `/workspaces/custom-config/webapp-logo/upload` | `workspace/workspace.py` |
| `GET` | `/workspaces/current/permission` | `workspace/workspace.py` |
| `GET` | `/workspaces/current/members` | `workspace/members.py` |
| `DELETE` | `/workspaces/current/members/<member_id>` | `workspace/members.py` |
| `PUT` | `/workspaces/current/members/<member_id>/update-role` | `workspace/members.py` |
| `POST` | `/workspaces/current/members/<member_id>/owner-transfer` | `workspace/members.py` |
| `POST` | `/workspaces/current/members/invite-email` | `workspace/members.py` |
| `POST` | `/workspaces/current/members/owner-transfer-check` | `workspace/members.py` |
| `POST` | `/workspaces/current/members/send-owner-transfer-confirm-email` | `workspace/members.py` |
| `GET` | `/workspaces/current/dataset-operators` | `workspace/members.py` |
| `GET,POST` | `/workspaces/current/default-model` | `workspace/models.py` |
| `GET` | `/workspaces/current/model-providers` | `workspace/model_providers.py` |
| `GET` | `/workspaces/<tenant_id>/model-providers/<provider>/<icon_type>/<lang>` | `workspace/model_providers.py` |
| `GET,POST` | `/workspaces/current/model-providers/<provider>/credentials` | `workspace/model_providers.py` |
| `POST` | `/workspaces/current/model-providers/<provider>/credentials/validate` | `workspace/model_providers.py` |
| `POST` | `/workspaces/current/model-providers/<provider>/credentials/switch` | `workspace/model_providers.py` |
| `POST` | `/workspaces/current/model-providers/<provider>/preferred-provider-type` | `workspace/model_providers.py` |
| `GET` | `/workspaces/current/model-providers/<provider>/checkout-url` | `workspace/model_providers.py` |
| `GET,POST` | `/workspaces/current/model-providers/<provider>/models` | `workspace/models.py` |
| `GET` | `/workspaces/current/model-providers/<provider>/models/credentials` | `workspace/models.py` |
| `POST` | `/workspaces/current/model-providers/<provider>/models/credentials/validate` | `workspace/models.py` |
| `POST` | `/workspaces/current/model-providers/<provider>/models/credentials/switch` | `workspace/models.py` |
| `GET` | `/workspaces/current/model-providers/<provider>/models/parameter-rules` | `workspace/models.py` |
| `GET` | `/workspaces/current/models/model-types/<model_type>` | `workspace/models.py` |
| `GET` | `/workspaces/current/agent-providers` | `workspace/agent_providers.py` |
| `GET` | `/workspaces/current/agent-provider/<provider_name>` | `workspace/agent_providers.py` |

### Workspaces — Tools

| Method | Path | File |
|--------|------|------|
| `GET` | `/workspaces/current/tool-providers` | `workspace/tool_providers.py` |
| `GET` | `/workspaces/current/tool-labels` | `workspace/tool_providers.py` |
| `GET` | `/workspaces/current/tools/builtin` | `workspace/tool_providers.py` |
| `GET` | `/workspaces/current/tools/api` | `workspace/tool_providers.py` |
| `GET` | `/workspaces/current/tools/workflow` | `workspace/tool_providers.py` |
| `GET` | `/workspaces/current/tools/mcp` | `workspace/tool_providers.py` |
| `GET` | `/workspaces/current/tool-provider/builtin/<provider>/info` | `workspace/tool_providers.py` |
| `GET` | `/workspaces/current/tool-provider/builtin/<provider>/icon` | `workspace/tool_providers.py` |
| `GET` | `/workspaces/current/tool-provider/builtin/<provider>/tools` | `workspace/tool_providers.py` |
| `GET,POST` | `/workspaces/current/tool-provider/builtin/<provider>/credentials` | `workspace/tool_providers.py` |
| `POST` | `/workspaces/current/tool-provider/builtin/<provider>/add` | `workspace/tool_providers.py` |
| `POST` | `/workspaces/current/tool-provider/builtin/<provider>/update` | `workspace/tool_providers.py` |
| `POST` | `/workspaces/current/tool-provider/builtin/<provider>/delete` | `workspace/tool_providers.py` |
| `GET` | `/workspaces/current/tool-provider/builtin/<provider>/credential/info` | `workspace/tool_providers.py` |
| `GET` | `/workspaces/current/tool-provider/builtin/<provider>/credential/schema/<credential_type>` | `workspace/tool_providers.py` |
| `POST` | `/workspaces/current/tool-provider/builtin/<provider>/default-credential` | `workspace/tool_providers.py` |
| `GET` | `/workspaces/current/tool-provider/builtin/<provider>/oauth/client-schema` | `workspace/tool_providers.py` |
| `GET,POST` | `/workspaces/current/tool-provider/builtin/<provider>/oauth/custom-client` | `workspace/tool_providers.py` |
| `POST` | `/workspaces/current/tool-provider/api/add` | `workspace/tool_providers.py` |
| `POST` | `/workspaces/current/tool-provider/api/update` | `workspace/tool_providers.py` |
| `POST` | `/workspaces/current/tool-provider/api/delete` | `workspace/tool_providers.py` |
| `GET` | `/workspaces/current/tool-provider/api/get` | `workspace/tool_providers.py` |
| `GET` | `/workspaces/current/tool-provider/api/tools` | `workspace/tool_providers.py` |
| `POST` | `/workspaces/current/tool-provider/api/schema` | `workspace/tool_providers.py` |
| `GET` | `/workspaces/current/tool-provider/api/remote` | `workspace/tool_providers.py` |
| `POST` | `/workspaces/current/tool-provider/api/test/pre` | `workspace/tool_providers.py` |
| `POST` | `/workspaces/current/tool-provider/workflow/create` | `workspace/tool_providers.py` |
| `POST` | `/workspaces/current/tool-provider/workflow/update` | `workspace/tool_providers.py` |
| `POST` | `/workspaces/current/tool-provider/workflow/delete` | `workspace/tool_providers.py` |
| `GET` | `/workspaces/current/tool-provider/workflow/get` | `workspace/tool_providers.py` |
| `GET` | `/workspaces/current/tool-provider/workflow/tools` | `workspace/tool_providers.py` |
| `POST` | `/workspaces/current/tool-provider/mcp` | `workspace/tool_providers.py` |
| `POST` | `/workspaces/current/tool-provider/mcp/auth` | `workspace/tool_providers.py` |
| `GET` | `/workspaces/current/tool-provider/mcp/tools/<provider_id>` | `workspace/tool_providers.py` |
| `GET` | `/workspaces/current/tool-provider/mcp/update/<provider_id>` | `workspace/tool_providers.py` |

### Workspaces — Triggers

| Method | Path | File |
|--------|------|------|
| `GET` | `/workspaces/current/triggers` | `workspace/trigger_providers.py` |
| `GET` | `/workspaces/current/trigger-provider/<provider>/info` | `workspace/trigger_providers.py` |
| `GET` | `/workspaces/current/trigger-provider/<provider>/icon` | `workspace/trigger_providers.py` |
| `GET` | `/workspaces/current/trigger-provider/<provider>/oauth/client` | `workspace/trigger_providers.py` |
| `GET` | `/workspaces/current/trigger-provider/<provider>/subscriptions/list` | `workspace/trigger_providers.py` |
| `GET` | `/workspaces/current/trigger-provider/<provider>/subscriptions/oauth/authorize` | `workspace/trigger_providers.py` |

### Workspaces — Plugins

| Method | Path | File |
|--------|------|------|
| `GET` | `/workspaces/current/plugin/list` | `workspace/plugin.py` |
| `POST` | `/workspaces/current/plugin/install/marketplace` | `workspace/plugin.py` |
| `POST` | `/workspaces/current/plugin/install/github` | `workspace/plugin.py` |
| `POST` | `/workspaces/current/plugin/install/pkg` | `workspace/plugin.py` |
| `POST` | `/workspaces/current/plugin/uninstall` | `workspace/plugin.py` |
| `POST` | `/workspaces/current/plugin/upgrade/marketplace` | `workspace/plugin.py` |
| `POST` | `/workspaces/current/plugin/upgrade/github` | `workspace/plugin.py` |
| `POST` | `/workspaces/current/plugin/upload/pkg` | `workspace/plugin.py` |
| `POST` | `/workspaces/current/plugin/upload/github` | `workspace/plugin.py` |
| `POST` | `/workspaces/current/plugin/upload/bundle` | `workspace/plugin.py` |
| `GET` | `/workspaces/current/plugin/tasks` | `workspace/plugin.py` |
| `GET` | `/workspaces/current/plugin/tasks/<task_id>` | `workspace/plugin.py` |
| `POST` | `/workspaces/current/plugin/tasks/<task_id>/delete` | `workspace/plugin.py` |
| `POST` | `/workspaces/current/plugin/tasks/<task_id>/delete/<identifier>` | `workspace/plugin.py` |
| `POST` | `/workspaces/current/plugin/tasks/delete_all` | `workspace/plugin.py` |
| `GET` | `/workspaces/current/plugin/fetch-manifest` | `workspace/plugin.py` |
| `GET` | `/workspaces/current/plugin/readme` | `workspace/plugin.py` |
| `GET` | `/workspaces/current/plugin/icon` | `workspace/plugin.py` |
| `GET` | `/workspaces/current/plugin/asset` | `workspace/plugin.py` |
| `GET` | `/workspaces/current/plugin/marketplace/pkg` | `workspace/plugin.py` |
| `POST` | `/workspaces/current/plugin/list/installations/ids` | `workspace/plugin.py` |
| `POST` | `/workspaces/current/plugin/list/latest-versions` | `workspace/plugin.py` |
| `GET` | `/workspaces/current/plugin/debugging-key` | `workspace/plugin.py` |
| `GET` | `/workspaces/current/plugin/permission/fetch` | `workspace/plugin.py` |
| `POST` | `/workspaces/current/plugin/permission/change` | `workspace/plugin.py` |
| `GET` | `/workspaces/current/plugin/preferences/fetch` | `workspace/plugin.py` |
| `POST` | `/workspaces/current/plugin/preferences/change` | `workspace/plugin.py` |
| `POST` | `/workspaces/current/plugin/preferences/autoupgrade/exclude` | `workspace/plugin.py` |
| `GET` | `/workspaces/current/plugin/parameters/dynamic-options` | `workspace/plugin.py` |
| `POST` | `/workspaces/current/plugin/parameters/dynamic-options-with-credentials` | `workspace/plugin.py` |

### Workspaces — Endpoints

| Method | Path | File |
|--------|------|------|
| `GET` | `/workspaces/current/endpoints` | `workspace/endpoint.py` |
| `POST` | `/workspaces/current/endpoints/create` | `workspace/endpoint.py` |
| `POST` | `/workspaces/current/endpoints/update` | `workspace/endpoint.py` |
| `POST` | `/workspaces/current/endpoints/delete` | `workspace/endpoint.py` |
| `POST` | `/workspaces/current/endpoints/enable` | `workspace/endpoint.py` |
| `POST` | `/workspaces/current/endpoints/disable` | `workspace/endpoint.py` |
| `GET` | `/workspaces/current/endpoints/list` | `workspace/endpoint.py` |
| `GET` | `/workspaces/current/endpoints/list/plugin` | `workspace/endpoint.py` |
| `DELETE` | `/workspaces/current/endpoints/<id>` | `workspace/endpoint.py` |

### Files & Remote Files

| Method | Path | File |
|--------|------|------|
| `GET,POST` | `/files/upload` | `files.py` |
| `GET` | `/files/<file_id>/preview` | `files.py` |
| `GET` | `/files/support-type` | `files.py` |
| `POST` | `/remote-files/upload` | `remote_files.py` |
| `GET` | `/remote-files/<url>` | `remote_files.py` |

### Tags

| Method | Path | File |
|--------|------|------|
| `GET,POST` | `/tags` | `tag/tags.py` |
| `PATCH,DELETE` | `/tags/<tag_id>` | `tag/tags.py` |
| `POST` | `/tag-bindings` | `tag/tags.py` |
| `POST` | `/tag-bindings/create` | `tag/tags.py` |
| `POST` | `/tag-bindings/remove` | `tag/tags.py` |
| `DELETE` | `/tag-bindings/<id>` | `tag/tags.py` |

### Explore

| Method | Path | File |
|--------|------|------|
| `GET` | `/explore/apps` | `explore/recommended_app.py` |
| `GET` | `/explore/apps/<app_id>` | `explore/recommended_app.py` |
| `GET` | `/installed-apps` | `explore/installed_app.py` |
| `DELETE,PATCH` | `/installed-apps/<installed_app_id>` | `explore/installed_app.py` |
| `GET` | `/installed-apps/<installed_app_id>/meta` | `explore/parameter.py` |
| `GET` | `/installed-apps/<installed_app_id>/parameters` | `explore/parameter.py` |
| `GET,POST` | `/installed-apps/<installed_app_id>/saved-messages` | `explore/saved_message.py` |
| `POST` | `/installed-apps/<installed_app_id>/workflows/run` | `explore/workflow.py` |
| `POST` | `/installed-apps/<installed_app_id>/workflows/tasks/<task_id>/stop` | `explore/workflow.py` |

### Generator & Templates

| Method | Path | File |
|--------|------|------|
| `POST` | `/instruction-generate` | `app/generator.py` |
| `POST` | `/instruction-generate/template` | `app/generator.py` |
| `POST` | `/rule-generate` | `app/generator.py` |
| `POST` | `/rule-code-generate` | `app/generator.py` |
| `POST` | `/rule-structured-output-generate` | `app/generator.py` |
| `GET` | `/app/prompt-templates` | `app/advanced_prompt_template.py` |

### Notifications & System

| Method | Path | File |
|--------|------|------|
| `GET` | `/notification` | `notification.py` |
| `POST` | `/notification/dismiss` | `notification.py` |
| `GET` | `/features` | `feature.py` |
| `GET` | `/system-features` | `feature.py` |
| `GET` | `/spec/schema-definitions` | `spec.py` |
| `GET` | `/form/human_input/<form_token>` | `human_input_form.py` |

### Billing

| Method | Path | File |
|--------|------|------|
| `GET` | `/billing/subscription` | `billing/billing.py` |
| `GET` | `/billing/invoices` | `billing/billing.py` |
| `PUT` | `/billing/partners/<partner_key>/tenants` | `billing/billing.py` |
| `GET` | `/compliance/download` | `billing/compliance.py` |

### Admin

| Method | Path | File |
|--------|------|------|
| `POST` | `/admin/batch_add_notification_accounts` | `admin.py` |
| `POST` | `/admin/insert-explore-apps` | `admin.py` |
| `DELETE` | `/admin/insert-explore-apps/<app_id>` | `admin.py` |
| `POST` | `/admin/insert-explore-banner` | `admin.py` |
| `DELETE` | `/admin/delete-explore-banner/<banner_id>` | `admin.py` |
| `POST` | `/admin/upsert_notification` | `admin.py` |

### API Key Auth

| Method | Path | File |
|--------|------|------|
| `GET` | `/api-key-auth/data-source` | `auth/data_source_bearer_auth.py` |
| `POST` | `/api-key-auth/data-source/binding` | `auth/data_source_bearer_auth.py` |
| `DELETE` | `/api-key-auth/data-source/<binding_id>` | `auth/data_source_bearer_auth.py` |
| `GET,POST` | `/api-based-extension` | `extension.py` |
| `GET,POST` | `/api-based-extension/<id>` | `extension.py` |
| `GET` | `/code-based-extension` | `extension.py` |

---

## Service API

> Base prefix: `/v1`  
> Auth: `Authorization: Bearer <api-key>`

### App Info

| Method | Path | File |
|--------|------|------|
| `GET` | `/info` | `app/app.py` |
| `GET` | `/parameters` | `app/app.py` |
| `GET` | `/meta` | `app/app.py` |
| `GET` | `/site` | `app/site.py` |

### Chat

| Method | Path | File |
|--------|------|------|
| `POST` | `/chat-messages` | `app/completion.py` |
| `POST` | `/chat-messages/<task_id>/stop` | `app/completion.py` |
| `GET` | `/messages` | `app/message.py` |
| `POST` | `/messages/<message_id>/feedbacks` | `app/message.py` |
| `GET` | `/messages/<message_id>/suggested` | `app/message.py` |
| `GET` | `/app/feedbacks` | `app/message.py` |
| `GET` | `/conversations` | `app/conversation.py` |
| `DELETE` | `/conversations/<c_id>` | `app/conversation.py` |
| `POST` | `/conversations/<c_id>/name` | `app/conversation.py` |
| `GET` | `/conversations/<c_id>/variables` | `app/conversation.py` |
| `PUT` | `/conversations/<c_id>/variables/<variable_id>` | `app/conversation.py` |

### Completion

| Method | Path | File |
|--------|------|------|
| `POST` | `/completion-messages` | `app/completion.py` |
| `POST` | `/completion-messages/<task_id>/stop` | `app/completion.py` |

### Workflow

| Method | Path | File |
|--------|------|------|
| `POST` | `/workflows/run` | `app/workflow.py` |
| `GET` | `/workflows/run/<workflow_run_id>` | `app/workflow.py` |
| `POST` | `/workflows/tasks/<task_id>/stop` | `app/workflow.py` |
| `GET` | `/workflows/logs` | `app/workflow.py` |
| `POST` | `/workflows/<workflow_id>/run` | `app/workflow.py` |
| `GET` | `/workflow/<task_id>/events` | `app/workflow_events.py` |

### Files & Audio

| Method | Path | File |
|--------|------|------|
| `POST` | `/files/upload` | `app/file.py` |
| `GET` | `/files/<file_id>/preview` | `app/file_preview.py` |
| `POST` | `/audio-to-text` | `app/audio.py` |
| `POST` | `/text-to-audio` | `app/audio.py` |

### Annotations

| Method | Path | File |
|--------|------|------|
| `GET` | `/apps/annotations` | `app/annotation.py` |
| `PUT` | `/apps/annotations/<annotation_id>` | `app/annotation.py` |
| `POST` | `/apps/annotation-reply/<action>` | `app/annotation.py` |
| `GET` | `/apps/annotation-reply/<action>/status/<job_id>` | `app/annotation.py` |

### Datasets

| Method | Path | File |
|--------|------|------|
| `GET` | `/datasets` | `dataset/dataset.py` |
| `POST` | `/datasets` | `dataset/dataset.py` |
| `GET` | `/datasets/<dataset_id>` | `dataset/dataset.py` |
| `DELETE` | `/datasets/<dataset_id>` | `dataset/dataset.py` |
| `PATCH` | `/datasets/<dataset_id>/documents/status/<action>` | `dataset/dataset.py` |
| `GET` | `/datasets/<dataset_id>/tags` | `dataset/dataset.py` |
| `GET,POST` | `/datasets/tags` | `dataset/dataset.py` |
| `POST` | `/datasets/tags/binding` | `dataset/dataset.py` |
| `POST` | `/datasets/tags/unbinding` | `dataset/dataset.py` |

### Datasets — Documents

| Method | Path | File |
|--------|------|------|
| `GET,POST` | `/datasets/<dataset_id>/documents` | `dataset/document.py` |
| `GET` | `/datasets/<dataset_id>/documents/<document_id>` | `dataset/document.py` |
| `DELETE` | `/datasets/<dataset_id>/documents/<document_id>` | `dataset/document.py` |
| `GET` | `/datasets/<dataset_id>/documents/<document_id>/download` | `dataset/document.py` |
| `GET` | `/datasets/<dataset_id>/documents/<batch>/indexing-status` | `dataset/document.py` |
| `POST` | `/datasets/<dataset_id>/document/create-by-text` | `dataset/document.py` |
| `POST` | `/datasets/<dataset_id>/document/create_by_text` | `dataset/document.py` _(deprecated alias)_ |
| `POST` | `/datasets/<dataset_id>/documents/<document_id>/update-by-text` | `dataset/document.py` |
| `POST` | `/datasets/<dataset_id>/documents/<document_id>/update_by_text` | `dataset/document.py` _(deprecated alias)_ |
| `POST` | `/datasets/<dataset_id>/documents/download-zip` | `dataset/document.py` |
| `POST` | `/datasets/<dataset_id>/documents/metadata` | `dataset/metadata.py` |

### Datasets — Segments

| Method | Path | File |
|--------|------|------|
| `POST` | `/datasets/<dataset_id>/documents/<document_id>/segments` | `dataset/segment.py` |
| `DELETE` | `/datasets/<dataset_id>/documents/<document_id>/segments/<segment_id>` | `dataset/segment.py` |

### Datasets — Metadata

| Method | Path | File |
|--------|------|------|
| `POST` | `/datasets/<dataset_id>/metadata` | `dataset/metadata.py` |
| `PATCH` | `/datasets/<dataset_id>/metadata/<metadata_id>` | `dataset/metadata.py` |
| `GET` | `/datasets/<dataset_id>/metadata/built-in` | `dataset/metadata.py` |
| `POST` | `/datasets/<dataset_id>/metadata/built-in/<action>` | `dataset/metadata.py` |

### Datasets — Hit Testing & Retrieval

| Method | Path | File |
|--------|------|------|
| `POST` | `/datasets/<dataset_id>/hit-testing` | `dataset/hit_testing.py` |
| `POST` | `/datasets/<dataset_id>/retrieve` | `dataset/hit_testing.py` |

### Datasets — RAG Pipeline

| Method | Path | File |
|--------|------|------|
| `POST` | `/datasets/<dataset_id>/pipeline/run` | `dataset/rag_pipeline/rag_pipeline_workflow.py` |
| `POST` | `/datasets/<dataset_id>/pipeline/datasource/nodes/<node_id>/run` | `dataset/rag_pipeline/rag_pipeline_workflow.py` |
| `GET` | `/datasets/<dataset_id>/pipeline/datasource-plugins` | `dataset/rag_pipeline/rag_pipeline_workflow.py` |
| `POST` | `/datasets/pipeline/file-upload` | `dataset/rag_pipeline/rag_pipeline_workflow.py` |

### End Users & Forms

| Method | Path | File |
|--------|------|------|
| `GET` | `/end-users/<end_user_id>` | `end_user/end_user.py` |
| `GET` | `/form/human_input/<form_token>` | `app/human_input_form.py` |

### Models

| Method | Path | File |
|--------|------|------|
| `GET` | `/workspaces/current/models/model-types/<model_type>` | `workspace/models.py` |
