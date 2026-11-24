api
├── AGENTS.md
├── API_ROUTES.md
├── Dockerfile
├── Dockerfile.dockerignore
├── README.md
├── **pycache**
│   ├── app.cpython-313.pyc
│   ├── app_factory.cpython-313.pyc
│   └── dify_app.cpython-313.pyc
├── app.py
├── app_factory.py
├── celery_entrypoint.py
├── celery_healthcheck.py
├── celerybeat-schedule
├── clients
│   ├── **init**.py
│   ├── **pycache**
│   └── agent_backend
├── cnt_base.sh
├── commands
│   ├── **init**.py
│   ├── **pycache**
│   ├── account.py
│   ├── data_migration.py
│   ├── knowledge_fs.py
│   ├── plugin.py
│   ├── rbac.py
│   ├── retention.py
│   ├── storage.py
│   ├── system.py
│   └── vector.py
├── configs
│   ├── **init**.py
│   ├── **pycache**
│   ├── app_config.py
│   ├── deploy
│   ├── enterprise
│   ├── extra
│   ├── feature
│   ├── middleware
│   ├── observability
│   ├── packaging
│   ├── remote_settings_sources
│   └── secret_key.py
├── conftest.py
├── constants
│   ├── **init**.py
│   ├── **pycache**
│   ├── dsl_version.py
│   ├── languages.py
│   ├── mimetypes.py
│   ├── model_template.py
│   ├── oauth_bearer.py
│   ├── pipeline_templates.json
│   ├── recommended_apps.json
│   └── resource_access_token.py
├── context
│   ├── **init**.py
│   ├── **pycache**
│   ├── execution_context.py
│   ├── flask_app_context.py
│   └── models.py
├── contexts
│   ├── **init**.py
│   ├── **pycache**
│   └── wrapper.py
├── controllers
│   ├── API_SCHEMA_GUIDE.md
│   ├── **init**.py
│   ├── **pycache**
│   ├── common
│   ├── console
│   ├── fastopenapi.py
│   ├── files
│   ├── inner_api
│   ├── mcp
│   ├── openapi
│   ├── service_api
│   ├── trigger
│   └── web
├── core
│   ├── **init**.py
│   ├── **pycache**
│   ├── agent
│   ├── app
│   ├── base
│   ├── callback_handler
│   ├── credit_usage.py
│   ├── datasource
│   ├── db
│   ├── entities
│   ├── errors
│   ├── extension
│   ├── external_data_tool
│   ├── file
│   ├── helper
│   ├── hosting_configuration.py
│   ├── llm_generator
│   ├── logging
│   ├── mcp
│   ├── memory
│   ├── model_context.py
│   ├── model_manager.py
│   ├── moderation
│   ├── network_access
│   ├── ops
│   ├── plugin
│   ├── prompt
│   ├── provider_manager.py
│   ├── rag
│   ├── rbac
│   ├── repositories
│   ├── schemas
│   ├── telemetry
│   ├── tools
│   ├── trigger
│   └── workflow
├── dev
│   ├── **init**.py
│   ├── check_knowledge_fs_coverage.py
│   ├── generate_fastopenapi_specs.py
│   ├── generate_knowledge_fs_contract.py
│   ├── generate_swagger_markdown_docs.py
│   ├── generate_swagger_specs.py
│   ├── knowledge_fs_product_contract.py
│   ├── lint_response_contracts.py
│   ├── pytest_sharding.md
│   └── pytest_sharding.py
├── dify_app.py
├── docker
│   └── entrypoint.sh
├── enterprise
│   ├── **init**.py
│   ├── **pycache**
│   └── telemetry
├── enums
│   ├── **init**.py
│   ├── **pycache**
│   └── account.py
├── events
│   ├── **init**.py
│   ├── **pycache**
│   ├── app_event.py
│   ├── dataset_event.py
│   ├── document_event.py
│   ├── document_index_event.py
│   ├── event_handlers
│   ├── message_event.py
│   └── tenant_event.py
├── extensions
│   ├── **init**.py
│   ├── **pycache**
│   ├── application_services
│   ├── ext_app_metrics.py
│   ├── ext_application_services.py
│   ├── ext_blueprints.py
│   ├── ext_celery.py
│   ├── ext_code_based_extension.py
│   ├── ext_commands.py
│   ├── ext_compress.py
│   ├── ext_database.py
│   ├── ext_enterprise_telemetry.py
│   ├── ext_fastopenapi.py
│   ├── ext_forward_refs.py
│   ├── ext_hosting_provider.py
│   ├── ext_import_modules.py
│   ├── ext_key_provider.py
│   ├── ext_knowledge_fs_observability.py
│   ├── ext_logging.py
│   ├── ext_login.py
│   ├── ext_logstore.py
│   ├── ext_mail.py
│   ├── ext_migrate.py
│   ├── ext_oauth_bearer.py
│   ├── ext_orjson.py
│   ├── ext_otel.py
│   ├── ext_proxy_fix.py
│   ├── ext_redis.py
│   ├── ext_request_logging.py
│   ├── ext_sentry.py
│   ├── ext_session_factory.py
│   ├── ext_set_secretkey.py
│   ├── ext_socketio.py
│   ├── ext_storage.py
│   ├── ext_timezone.py
│   ├── ext_warnings.py
│   ├── logstore
│   ├── otel
│   ├── redis_names.py
│   ├── storage
│   └── workflow_warm_shutdown.py
├── factories
│   ├── **init**.py
│   ├── **pycache**
│   ├── agent_factory.py
│   ├── file_factory
│   └── variable_factory.py
├── fields
│   ├── **init**.py
│   ├── **pycache**
│   ├── _value_type_serializer.py
│   ├── agent_fields.py
│   ├── annotation_fields.py
│   ├── api_key_fields.py
│   ├── app_fields.py
│   ├── app_model_config_response.py
│   ├── base.py
│   ├── conversation_fields.py
│   ├── conversation_variable_fields.py
│   ├── dataset_fields.py
│   ├── document_fields.py
│   ├── end_user_fields.py
│   ├── file_fields.py
│   ├── file_grant_fields.py
│   ├── hit_testing_fields.py
│   ├── member_fields.py
│   ├── message_fields.py
│   ├── segment_fields.py
│   ├── snippet_fields.py
│   ├── workflow_draft_variable_fields.py
│   └── workflow_run_fields.py
├── gunicorn.conf.py
├── knowledge-fs-contract
│   ├── README.md
│   ├── dify-capability-v2-auth-profile.json
│   ├── dify-capability-v2-operations.json
│   ├── dify-capability-v2-test-vector.json
│   ├── knowledge-fs.openapi.json
│   └── source-provenance.json
├── knowledge-fs-contract.lock.json
├── knowledge-fs-product-operation-gaps.json
├── knowledge-fs-product-operations.json
├── libs
│   ├── **init**.py
│   ├── **pycache**
│   ├── archive_storage.py
│   ├── broadcast_channel
│   ├── collection_utils.py
│   ├── contextvars.py
│   ├── custom_inputs.py
│   ├── datetime_utils.py
│   ├── db_migration_lock.py
│   ├── device_flow_security.py
│   ├── email_i18n.py
│   ├── email_template_renderer.py
│   ├── encryption.py
│   ├── exception.py
│   ├── external_api.py
│   ├── file_utils.py
│   ├── flask_restx_compat.py
│   ├── flask_utils.py
│   ├── gmpy2_pkcs10aep_cipher.py
│   ├── helper.py
│   ├── infinite_scroll_pagination.py
│   ├── json_in_md_parser.py
│   ├── jws.py
│   ├── key_providers
│   ├── login.py
│   ├── module_loading.py
│   ├── oauth.py
│   ├── oauth_bearer.py
│   ├── orjson.py
│   ├── pagination.py
│   ├── passport.py
│   ├── password.py
│   ├── pyrefly_diagnostics.py
│   ├── pyrefly_type_coverage.py
│   ├── rate_limit.py
│   ├── rsa.py
│   ├── schedule_utils.py
│   ├── sendgrid.py
│   ├── smtp.py
│   ├── stream.py
│   ├── time_parser.py
│   ├── token.py
│   ├── url_utils.py
│   ├── uuid_utils.py
│   ├── validators.py
│   ├── workspace_permission.py
│   └── zip_filename_recovery.py
├── machinery
│   ├── **init**.py
│   ├── **pycache**
│   ├── context.py
│   └── errors.py
├── migrations
│   ├── README
│   ├── **pycache**
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
├── models
│   ├── **init**.py
│   ├── **pycache**
│   ├── _workflow_exc.py
│   ├── account.py
│   ├── agent.py
│   ├── agent_config_entities.py
│   ├── agent_sandbox_usage.py
│   ├── api_based_extension.py
│   ├── application_trace.py
│   ├── base.py
│   ├── comment.py
│   ├── credential_permission.py
│   ├── dataset.py
│   ├── engine.py
│   ├── enums.py
│   ├── execution_extra_content.py
│   ├── human_input.py
│   ├── knowledge_fs.py
│   ├── knowledge_fs_cleanup.py
│   ├── knowledge_fs_cutover.py
│   ├── model.py
│   ├── oauth.py
│   ├── onboarding.py
│   ├── provider.py
│   ├── provider_ids.py
│   ├── resource_access_token.py
│   ├── skill.py
│   ├── snippet.py
│   ├── source.py
│   ├── task.py
│   ├── tools.py
│   ├── trigger.py
│   ├── types.py
│   ├── utils
│   ├── web.py
│   └── workflow.py
├── openapi
│   └── markdown
├── providers
│   ├── README.md
│   ├── conftest.py
│   ├── trace
│   └── vdb
├── pyproject.toml
├── pyrefly-local-excludes.txt
├── pytest.ini
├── repositories
│   ├── **init**.py
│   ├── **pycache**
│   ├── account
│   ├── account_activation_repository.py
│   ├── account_integration_repository.py
│   ├── agent_workspace_repository.py
│   ├── api_based_extension_repository.py
│   ├── api_workflow_node_execution_repository.py
│   ├── api_workflow_run_repository.py
│   ├── app
│   ├── app_definition_query_repository.py
│   ├── app_preview_query_repository.py
│   ├── app_scoped_end_user_repository.py
│   ├── app_statistic_query_repository.py
│   ├── application_trace_repository.py
│   ├── conversation_lifecycle.py
│   ├── conversation_variable_query_repository.py
│   ├── credentials
│   ├── data_source
│   ├── entities
│   ├── execution_extra_content_repository.py
│   ├── explore_banner_query_repository.py
│   ├── factory.py
│   ├── file_grant_repository.py
│   ├── human_input_errors.py
│   ├── human_input_file_upload_repository.py
│   ├── installation_state_repository.py
│   ├── installed_app_conversation_repository.py
│   ├── installed_app_message_repository.py
│   ├── installed_app_repository.py
│   ├── knowledge
│   ├── knowledge_fs_cleanup_repository.py
│   ├── knowledge_fs_control_space_repository.py
│   ├── knowledge_fs_cutover_repository.py
│   ├── knowledge_fs_lifecycle_outbox_repository.py
│   ├── message_file_preview_repository.py
│   ├── network_access_group_repository.py
│   ├── oauth_access_token_repository.py
│   ├── oauth_device_token_repository.py
│   ├── oauth_server_repository.py
│   ├── plugin_file_upload_repository.py
│   ├── recommended_app_catalog_repository.py
│   ├── resource_access_token_repository.py
│   ├── saved_message_repository.py
│   ├── sqlalchemy_api_workflow_node_execution_repository.py
│   ├── sqlalchemy_api_workflow_run_repository.py
│   ├── sqlalchemy_execution_extra_content_repository.py
│   ├── sqlalchemy_knowledge_fs_capability_issuance_auditor.py
│   ├── sqlalchemy_knowledge_fs_capability_issuance_reservation_repository.py
│   ├── sqlalchemy_knowledge_fs_cleanup_repository.py
│   ├── sqlalchemy_knowledge_fs_control_space_repository.py
│   ├── sqlalchemy_knowledge_fs_control_space_state_metrics.py
│   ├── sqlalchemy_knowledge_fs_cutover_repository.py
│   ├── sqlalchemy_knowledge_fs_lifecycle_outbox_repository.py
│   ├── sqlalchemy_workflow_trigger_log_repository.py
│   ├── step_by_step_tour_repository.py
│   ├── tag_repository.py
│   ├── trial_app_repository.py
│   ├── trigger
│   ├── types.py
│   ├── upload_file_delivery_repository.py
│   ├── web_passport_repository.py
│   ├── webapp_access_query_repository.py
│   ├── workflow_app_log_query_repository.py
│   ├── workflow_collaboration_repository.py
│   ├── workflow_run_archive_repository.py
│   ├── workflow_run_control.py
│   ├── workflow_tool_source_repository.py
│   ├── workflow_trigger_log_repository.py
│   └── workspace
├── schedule
│   ├── **pycache**
│   ├── check_upgradable_plugin_task.py
│   ├── clean_embedding_cache_task.py
│   ├── clean_messages.py
│   ├── clean_oauth_access_tokens_task.py
│   ├── clean_unused_datasets_task.py
│   ├── clean_workflow_runlogs_precise.py
│   ├── clean_workflow_runs_task.py
│   ├── collect_agent_sandbox_usage.py
│   ├── create_tidb_serverless_task.py
│   ├── mail_clean_document_notify_task.py
│   ├── queue_monitor_task.py
│   ├── trigger_provider_refresh_task.py
│   ├── update_api_token_last_used_task.py
│   ├── update_tidb_serverless_status_task.py
│   └── workflow_schedule_task.py
├── services
│   ├── **init**.py
│   ├── **pycache**
│   ├── account
│   ├── account_access_service.py
│   ├── account_activation_service.py
│   ├── account_avatar_file_gateway.py
│   ├── account_avatar_service.py
│   ├── account_change_email_ports.py
│   ├── account_change_email_service.py
│   ├── account_deletion_feedback_service.py
│   ├── account_deletion_service.py
│   ├── account_education_service.py
│   ├── account_email.py
│   ├── account_errors.py
│   ├── account_initialization_service.py
│   ├── account_integration_service.py
│   ├── account_password_hasher.py
│   ├── account_password_service.py
│   ├── account_ports.py
│   ├── account_profile_service.py
│   ├── account_security_gateway.py
│   ├── agent
│   ├── agent_config_service.py
│   ├── agent_llm_inner_service.py
│   ├── agent_service.py
│   ├── agent_tool_inner_service.py
│   ├── agent_tracing_config_service.py
│   ├── annotation_service.py
│   ├── api_based_extension_adapters.py
│   ├── api_based_extension_application_service.py
│   ├── api_token_service.py
│   ├── app
│   ├── app_audio_adapters.py
│   ├── app_audio_service.py
│   ├── app_creation_records.py
│   ├── app_definition_query_service.py
│   ├── app_dsl_service.py
│   ├── app_generate_service.py
│   ├── app_import_source.py
│   ├── app_model_config_service.py
│   ├── app_package_service.py
│   ├── app_preview_details_adapters.py
│   ├── app_preview_details_service.py
│   ├── app_preview_query_service.py
│   ├── app_ref_service.py
│   ├── app_scoped_end_user_query_service.py
│   ├── app_scoped_end_user_service.py
│   ├── app_service.py
│   ├── app_site_service.py
│   ├── app_statistic_query.py
│   ├── app_storage_cleanup_service.py
│   ├── app_task_service.py
│   ├── app_tracing_config_gateway.py
│   ├── app_tracing_config_service.py
│   ├── async_workflow_service.py
│   ├── attachment_service.py
│   ├── audio_provider_gateway.py
│   ├── audio_service.py
│   ├── audio_types.py
│   ├── auth
│   ├── billing_portal_service.py
│   ├── billing_service.py
│   ├── clear_free_plan_tenant_expired_logs.py
│   ├── code_based_extension_service.py
│   ├── compliance_download_service.py
│   ├── conversation_service.py
│   ├── conversation_variable_query.py
│   ├── conversation_variable_updater.py
│   ├── credentials
│   ├── credit_pool_service.py
│   ├── data_migration
│   ├── data_source
│   ├── dataset_knowledge_fs_upgrade_file_lease.py
│   ├── dataset_knowledge_fs_upgrade_service.py
│   ├── dataset_storage_cleanup_service.py
│   ├── document_indexing_proxy
│   ├── dsl_content.py
│   ├── dsl_version.py
│   ├── email_code_login_challenge.py
│   ├── enterprise
│   ├── entities
│   ├── errors
│   ├── explore_banner_query_service.py
│   ├── feature_query_service.py
│   ├── feature_service.py
│   ├── feature_service_gateway.py
│   ├── file_grant_gateways.py
│   ├── file_grant_service.py
│   ├── file_request_service.py
│   ├── file_service.py
│   ├── hit_testing_service.py
│   ├── human_input_delivery_test_service.py
│   ├── human_input_file_upload_service.py
│   ├── human_input_service.py
│   ├── icon_configuration.py
│   ├── init_validation_service.py
│   ├── inner_mail_service.py
│   ├── installed_app_access_service.py
│   ├── installed_app_conversation_service.py
│   ├── installed_app_generation_adapters.py
│   ├── installed_app_generation_service.py
│   ├── installed_app_message_adapters.py
│   ├── installed_app_message_service.py
│   ├── installed_app_service.py
│   ├── knowledge
│   ├── knowledge_fs
│   ├── knowledge_fs_capability.py
│   ├── knowledge_rate_limit_service.py
│   ├── knowledge_retrieval_inner_service.py
│   ├── legacy_model_type_migration.py
│   ├── message_file_preview_service.py
│   ├── message_service.py
│   ├── message_suggested_questions_adapters.py
│   ├── message_suggested_questions_service.py
│   ├── model_load_balancing_service.py
│   ├── model_provider
│   ├── network_access_group_gateway.py
│   ├── network_access_group_service.py
│   ├── notification_gateway.py
│   ├── notification_service.py
│   ├── oauth_device_adapters.py
│   ├── oauth_device_application_service.py
│   ├── oauth_device_contracts.py
│   ├── oauth_device_flow.py
│   ├── oauth_server_service.py
│   ├── openapi
│   ├── operation_service.py
│   ├── plugin
│   ├── plugin_file_upload_gateway.py
│   ├── plugin_file_upload_service.py
│   ├── quota_service.py
│   ├── rag_pipeline
│   ├── rbac
│   ├── rbac_agent_access_service.py
│   ├── recommended_app_catalog_gateway.py
│   ├── recommended_app_package_service.py
│   ├── recommended_app_query_service.py
│   ├── remote_file_service.py
│   ├── resource_access_token_service.py
│   ├── retention
│   ├── saved_message_service.py
│   ├── schema_definition_service.py
│   ├── setup_adapters.py
│   ├── setup_service.py
│   ├── skill_management_service.py
│   ├── snippet_dsl_service.py
│   ├── snippet_generate_service.py
│   ├── snippet_service.py
│   ├── step_by_step_tour_service.py
│   ├── system_feature_service.py
│   ├── tag_application_service.py
│   ├── tag_service.py
│   ├── telemetry_service.py
│   ├── tidb_binding_service.py
│   ├── tool_file_download_service.py
│   ├── tools
│   ├── tracing
│   ├── trial_app_access_service.py
│   ├── trial_app_generation_adapters.py
│   ├── trial_app_generation_service.py
│   ├── trial_app_usage.py
│   ├── trigger
│   ├── turnstile_service.py
│   ├── upload_file_delivery_service.py
│   ├── variable_truncator.py
│   ├── vector_space_admission_service.py
│   ├── web_app_runtime_query_service.py
│   ├── web_authentication_adapters.py
│   ├── web_authentication_service.py
│   ├── web_conversation_service.py
│   ├── web_passport_gateways.py
│   ├── web_passport_service.py
│   ├── webapp_access_adapters.py
│   ├── webapp_access_query_service.py
│   ├── webapp_auth_service.py
│   ├── workflow
│   ├── workflow_app_log_query_service.py
│   ├── workflow_collaboration_service.py
│   ├── workflow_draft_variable_service.py
│   ├── workflow_event_snapshot_service.py
│   ├── workflow_generator_service.py
│   ├── workflow_node_execution_trace_service.py
│   ├── workflow_node_variables.py
│   ├── workflow_persistence.py
│   ├── workflow_ref_service.py
│   ├── workflow_restore.py
│   ├── workflow_run_agg.py
│   ├── workflow_run_index.py
│   ├── workflow_run_service.py
│   ├── workflow_service.py
│   ├── workflow_statistic_query_service.py
│   ├── workflow_tool_source_service.py
│   ├── workflow_variable_reference_validator.py
│   ├── workflow_version_number_service.py
│   └── workspace
├── tasks
│   ├── **init**.py
│   ├── **pycache**
│   ├── add_document_to_index_task.py
│   ├── annotation
│   ├── app_generate
│   ├── application_trace_task.py
│   ├── async_workflow_tasks.py
│   ├── batch_clean_document_task.py
│   ├── batch_create_segment_to_index_task.py
│   ├── clean_dataset_task.py
│   ├── clean_document_task.py
│   ├── clean_notion_document_task.py
│   ├── collect_agent_resources_task.py
│   ├── community_telemetry_task.py
│   ├── create_segment_to_index_task.py
│   ├── deal_dataset_index_update_task.py
│   ├── deal_dataset_vector_index_task.py
│   ├── delete_account_task.py
│   ├── delete_conversation_task.py
│   ├── delete_segment_from_index_task.py
│   ├── disable_segment_from_index_task.py
│   ├── disable_segments_from_index_task.py
│   ├── document_indexing_sync_task.py
│   ├── document_indexing_task.py
│   ├── document_indexing_update_task.py
│   ├── duplicate_document_indexing_task.py
│   ├── enable_segment_to_index_task.py
│   ├── enable_segments_to_index_task.py
│   ├── enterprise_telemetry_task.py
│   ├── generate_summary_index_task.py
│   ├── human_input_timeout_tasks.py
│   ├── initialize_created_app_rbac_access_task.py
│   ├── install_default_plugins_task.py
│   ├── knowledge_fs_agent_investigation_tasks.py
│   ├── knowledge_fs_background_tasks.py
│   ├── knowledge_fs_failed_retrieval_tasks.py
│   ├── knowledge_fs_initial_source_preview_tasks.py
│   ├── knowledge_fs_initial_source_tasks.py
│   ├── knowledge_fs_lifecycle_tasks.py
│   ├── knowledge_fs_source_import_tasks.py
│   ├── knowledge_fs_upgrade_tasks.py
│   ├── mail_account_deletion_task.py
│   ├── mail_change_mail_task.py
│   ├── mail_email_code_login.py
│   ├── mail_human_input_delivery_task.py
│   ├── mail_inner_task.py
│   ├── mail_invite_member_task.py
│   ├── mail_owner_transfer_task.py
│   ├── mail_register_task.py
│   ├── mail_reset_password_task.py
│   ├── mail_workflow_comment_task.py
│   ├── ops_trace_task.py
│   ├── process_tenant_plugin_autoupgrade_check_task.py
│   ├── rag_pipeline
│   ├── recover_document_indexing_task.py
│   ├── refresh_billing_vector_space_task.py
│   ├── regenerate_summary_index_task.py
│   ├── remove_app_and_related_data_task.py
│   ├── remove_document_from_index_task.py
│   ├── retry_document_indexing_task.py
│   ├── sync_website_document_indexing_task.py
│   ├── trigger_processing_tasks.py
│   ├── trigger_subscription_refresh_tasks.py
│   ├── workflow_cfs_scheduler
│   ├── workflow_draft_var_tasks.py
│   ├── workflow_execution_tasks.py
│   ├── workflow_node_execution_tasks.py
│   ├── workflow_run_archive_deletion_tasks.py
│   ├── workflow_run_archive_download_tasks.py
│   └── workflow_schedule_tasks.py
├── templates
│   ├── change_mail_completed_template_en-US.html
│   ├── change_mail_completed_template_zh-CN.html
│   ├── change_mail_confirm_new_template_en-US.html
│   ├── change_mail_confirm_new_template_zh-CN.html
│   ├── change_mail_confirm_old_template_en-US.html
│   ├── change_mail_confirm_old_template_zh-CN.html
│   ├── clean_document_job_mail_template-US.html
│   ├── delete_account_code_email_template_en-US.html
│   ├── delete_account_success_template_en-US.html
│   ├── email_code_login_mail_template_en-US.html
│   ├── email_code_login_mail_template_zh-CN.html
│   ├── invite_member_mail_template_en-US.html
│   ├── invite_member_mail_template_zh-CN.html
│   ├── queue_monitor_alert_email_template_en-US.html
│   ├── register_email_template_en-US.html
│   ├── register_email_template_zh-CN.html
│   ├── register_email_when_account_exist_template_en-US.html
│   ├── register_email_when_account_exist_template_zh-CN.html
│   ├── reset_password_mail_template_en-US.html
│   ├── reset_password_mail_template_zh-CN.html
│   ├── reset_password_mail_when_account_not_exist_no_register_template_en-US.html
│   ├── reset_password_mail_when_account_not_exist_no_register_template_zh-CN.html
│   ├── reset_password_mail_when_account_not_exist_template_en-US.html
│   ├── reset_password_mail_when_account_not_exist_template_zh-CN.html
│   ├── transfer_workspace_new_owner_notify_template_en-US.html
│   ├── transfer_workspace_new_owner_notify_template_zh-CN.html
│   ├── transfer_workspace_old_owner_notify_template_en-US.html
│   ├── transfer_workspace_old_owner_notify_template_zh-CN.html
│   ├── transfer_workspace_owner_confirm_template_en-US.html
│   ├── transfer_workspace_owner_confirm_template_zh-CN.html
│   ├── without-brand
│   ├── workflow_comment_mention_template_en-US.html
│   └── workflow_comment_mention_template_zh-CN.html
├── tests
│   ├── **init**.py
│   ├── conftest.py
│   ├── fixtures
│   ├── helpers
│   ├── integration_tests
│   ├── knowledge_fs_vector_integration
│   ├── pytest_dify.py
│   ├── pytest_timing.py
│   ├── seed_legacy_model_type_dirty_data.py
│   ├── test_containers_integration_tests
│   ├── tool_fixtures.py
│   ├── unit_tests
│   └── workflow_test_utils.py
└── uv.lock
web
├── AGENTS.md
├── Dockerfile
├── Dockerfile.dockerignore
├── README.md
├── **mocks**
│   ├── @tanstack
│   └── zustand.ts
├── **tests**
│   ├── access-control
│   ├── api-key-management.spec.tsx
│   ├── base
│   ├── billing
│   ├── embed.spec.ts
│   ├── embedded-user-id-auth.test.tsx
│   ├── embedded-user-id-store.test.tsx
│   ├── env.spec.ts
│   ├── file-supported-formats.spec.tsx
│   ├── interactive-component-mock-boundary.spec.ts
│   ├── proxy-frame-options.spec.ts
│   └── workflow
├── app
│   ├── (commonLayout)
│   ├── (education)
│   ├── (humanInputLayout)
│   ├── (shareLayout)
│   ├── **tests**
│   ├── account
│   ├── activate
│   ├── auth
│   ├── components
│   ├── device
│   ├── education
│   ├── error.tsx
│   ├── forgot-password
│   ├── get-query-client.ts
│   ├── init
│   ├── install
│   ├── layout.tsx
│   ├── notifications
│   ├── oauth-callback
│   ├── query-provider.tsx
│   ├── query-state-provider.tsx
│   ├── reset-password
│   ├── route-metadata.ts
│   ├── signin
│   ├── signup
│   ├── styles
│   └── webapp-unavailable
├── assets
│   ├── action.svg
│   ├── csv.svg
│   ├── delete.svg
│   ├── doc.svg
│   ├── docx.svg
│   ├── html.svg
│   ├── json.svg
│   ├── md.svg
│   ├── pdf.svg
│   ├── search-menu.svg
│   ├── txt.svg
│   └── xlsx.svg
├── bin
│   └── uglify-embed.js
├── config
│   ├── **tests**
│   ├── index.spec.ts
│   ├── index.ts
│   └── server.ts
├── constants
│   └── link.ts
├── context
│   ├── **tests**
│   ├── app-context-defaults.ts
│   ├── app-context-normalizers.ts
│   ├── app-context-types.ts
│   ├── dataset-detail.ts
│   ├── debug-configuration.ts
│   ├── event-emitter-provider.tsx
│   ├── event-emitter.ts
│   ├── hooks
│   ├── i18n.spec.ts
│   ├── i18n.ts
│   ├── modal-context-provider.tsx
│   ├── modal-context.test.tsx
│   ├── modal-context.ts
│   ├── permission-state.ts
│   ├── web-app-context.tsx
│   └── workspace-state.ts
├── dev-proxy.config.ts
├── docker
│   └── entrypoint.sh
├── docs
│   ├── bundle-size.md
│   ├── hotkeys.md
│   ├── landmarks.md
│   ├── lint.md
│   ├── test.md
│   ├── toasts.md
│   ├── truncated-text-disclosure.md
│   └── webapp-document-gate.md
├── env.ts
├── features
│   ├── account-profile
│   ├── agent-v2
│   ├── app-access-error
│   ├── code-based-extension
│   ├── home
│   ├── knowledge-fs-availability
│   ├── network-access
│   ├── new-rag
│   ├── skills
│   ├── studio-list-navigation
│   ├── system-features
│   └── tag-management
├── global.d.ts
├── hooks
│   ├── **tests**
│   ├── use-api-access-url.ts
│   ├── use-app-favicon.spec.ts
│   ├── use-app-favicon.ts
│   ├── use-async-window-open.spec.ts
│   ├── use-async-window-open.ts
│   ├── use-breakpoints.spec.ts
│   ├── use-breakpoints.ts
│   ├── use-credential-permissions.spec.ts
│   ├── use-credential-permissions.ts
│   ├── use-document-title.spec.ts
│   ├── use-document-title.ts
│   ├── use-format-time-from-now.spec.ts
│   ├── use-format-time-from-now.ts
│   ├── use-i18n.ts
│   ├── use-import-dsl.spec.tsx
│   ├── use-import-dsl.ts
│   ├── use-knowledge.ts
│   ├── use-metadata.ts
│   ├── use-mitt.spec.ts
│   ├── use-mitt.ts
│   ├── use-oauth.ts
│   ├── use-pay.tsx
│   ├── use-query-params.spec.tsx
│   ├── use-query-params.ts
│   ├── use-theme.ts
│   ├── use-timestamp.spec.ts
│   └── use-timestamp.ts
├── i18n
│   ├── README.md
│   ├── **tests**
│   ├── client.ts
│   ├── index.ts
│   ├── language.ts
│   ├── languages.ts
│   ├── lib.client.ts
│   ├── lib.server.ts
│   ├── load-resource.ts
│   ├── locale-resources
│   ├── locale.ts
│   ├── locales
│   ├── metadata.ts
│   ├── resources.generated.d.ts
│   ├── resources.ts
│   ├── server.ts
│   ├── settings.ts
│   └── streamed-resources.ts
├── instrumentation-client.ts
├── instrumentation.ts
├── models
│   ├── access-control.ts
│   ├── app.ts
│   ├── common.ts
│   ├── datasets.ts
│   ├── debug.ts
│   ├── log.ts
│   ├── permission.ts
│   ├── pipeline.ts
│   ├── share.ts
│   └── snippet.ts
├── next
│   ├── headers.ts
│   ├── index.ts
│   ├── link.ts
│   ├── navigation.ts
│   ├── script.ts
│   └── server.ts
├── next-env.d.ts
├── next.config.ts
├── package.json
├── plugins
│   └── vite
├── postcss.config.mjs
├── proxy.ts
├── public
│   ├── education
│   ├── embed.js
│   ├── embed.min.js
│   ├── emoji
│   ├── favicon.ico
│   ├── illustrations
│   ├── images
│   ├── in-site-message
│   ├── logo
│   ├── marketplace
│   ├── pdf.worker.min.mjs
│   ├── screenshots
│   └── vs
├── scripts
│   ├── **tests**
│   ├── analyze-i18n-diff.ts
│   ├── bundle-analysis.ts
│   ├── check-i18n-values.ts
│   ├── check-i18n.js
│   ├── copy-and-start.mjs
│   ├── gen-doc-paths.ts
│   ├── generate-i18n-types.ts
│   ├── generate-provider-initials.ts
│   ├── migrate-i18n-selectors.ts
│   └── tsconfig.json
├── service
│   ├── **tests**
│   ├── access-control
│   ├── annotation.spec.ts
│   ├── annotation.ts
│   ├── app-deletion.ts
│   ├── base.spec.ts
│   ├── base.ts
│   ├── client-error.ts
│   ├── common.spec.ts
│   ├── common.ts
│   ├── console
│   ├── datasets.ts
│   ├── debug.ts
│   ├── device-flow.ts
│   ├── fetch.spec.ts
│   ├── fetch.ts
│   ├── http-error.spec.ts
│   ├── http-error.ts
│   ├── knowledge
│   ├── knowledge-fs
│   ├── log.ts
│   ├── marketplace-template-discovery.spec.ts
│   ├── marketplace-template-discovery.ts
│   ├── marketplace-templates.ts
│   ├── marketplace.ts
│   ├── plugins.spec.ts
│   ├── plugins.ts
│   ├── refresh-token.spec.ts
│   ├── refresh-token.ts
│   ├── request-error-toast.ts
│   ├── request-guard.ts
│   ├── share.spec.ts
│   ├── share.ts
│   ├── sso.ts
│   ├── tools.ts
│   ├── try-app.ts
│   ├── use-base.ts
│   ├── use-common.ts
│   ├── use-plugins-auth.ts
│   ├── use-plugins.ts
│   ├── use-share.spec.tsx
│   ├── use-share.ts
│   ├── use-snippet-workflows.ts
│   ├── use-snippets.ts
│   ├── use-triggers.ts
│   ├── use-try-app.ts
│   ├── use-workflow.ts
│   ├── webapp-address.spec.ts
│   ├── webapp-address.ts
│   ├── webapp-auth.spec.ts
│   ├── webapp-auth.ts
│   ├── workflow-generator.ts
│   ├── workflow-queries.ts
│   ├── workflow.spec.ts
│   └── workflow.ts
├── test
│   ├── **tests**
│   ├── button.ts
│   ├── console
│   ├── debug-configuration.tsx
│   ├── deferred.ts
│   ├── download.ts
│   ├── emoji-picker.ts
│   ├── fixtures
│   ├── i18n-mock.ts
│   ├── image-fetch.ts
│   ├── intersection-observer.ts
│   ├── knowledge-space.ts
│   ├── nuqs-testing.tsx
│   ├── pipeline-variables.ts
│   ├── query-atom.ts
│   ├── query-client.ts
│   ├── query-state-testing-adapter.tsx
│   ├── query-state-testing.tsx
│   └── workflow-editor.tsx
├── themes
│   ├── manual-dark.css
│   ├── manual-light.css
│   └── markdown.css
├── tsconfig.json
├── tsslint.config.ts
├── types
│   ├── app.ts
│   ├── assets.d.ts
│   ├── dataset.ts
│   ├── doc-paths.ts
│   ├── i18n.d.ts
│   ├── model-provider.ts
│   ├── pipeline.tsx
│   ├── snippet.ts
│   └── workflow.ts
├── utils
│   ├── **tests**
│   ├── app-redirection.spec.ts
│   ├── app-redirection.ts
│   ├── avatar.spec.ts
│   ├── avatar.ts
│   ├── client.ts
│   ├── clipboard.spec.ts
│   ├── clipboard.ts
│   ├── completion-params.spec.ts
│   ├── completion-params.ts
│   ├── create-app-tracking.ts
│   ├── document-title.ts
│   ├── download.spec.ts
│   ├── download.ts
│   ├── draft-07.json
│   ├── emoji-legacy.json
│   ├── emoji.ts
│   ├── encryption.ts
│   ├── error-message.ts
│   ├── error-parser.ts
│   ├── format.spec.ts
│   ├── format.ts
│   ├── get-icon.ts
│   ├── gtag.ts
│   ├── imported-app-redirection.spec.ts
│   ├── imported-app-redirection.ts
│   ├── index.spec.ts
│   ├── index.ts
│   ├── is-abort-error.ts
│   ├── login-redirect.client.ts
│   ├── login-redirect.ts
│   ├── marketplace-site-track.ts
│   ├── mcp.ts
│   ├── model-config.spec.ts
│   ├── model-config.ts
│   ├── object.ts
│   ├── page-leave-guard.ts
│   ├── permission.spec.ts
│   ├── permission.ts
│   ├── plugin-version-feature.ts
│   ├── provider-reference.ts
│   ├── query-atoms.spec.ts
│   ├── query-atoms.ts
│   ├── semver.spec.ts
│   ├── semver.ts
│   ├── time.ts
│   ├── timezone.json
│   ├── timezone.ts
│   ├── tool-call.ts
│   ├── urlValidation.spec.ts
│   ├── urlValidation.ts
│   ├── validators.spec.ts
│   ├── validators.ts
│   ├── var.spec.ts
│   ├── var.ts
│   ├── yaml.spec.ts
│   └── yaml.ts
├── vite.config.ts
├── vitest.browser.setup.ts
└── vitest.setup.ts
docker
├── README.md
├── certbot
│   ├── README.md
│   ├── docker-entrypoint.sh
│   └── update-cert.template.txt
├── couchbase-server
│   ├── Dockerfile
│   └── init-cbserver.sh
├── dify-env-sync.py
├── dify-env-sync.sh
├── docker-compose-template.yaml
├── docker-compose.e2b.yaml
├── docker-compose.middleware.yaml
├── docker-compose.png
├── docker-compose.pytest.middleware.yaml
├── docker-compose.pytest.ports.yaml
├── docker-compose.yaml
├── elasticsearch
│   └── docker-entrypoint.sh
├── envs
│   ├── core-services
│   ├── databases
│   ├── infrastructure
│   ├── middleware.env.example
│   ├── security.env.example
│   └── vectorstores
├── generate_docker_compose
├── iris
│   ├── docker-entrypoint.sh
│   └── iris-init.script
├── knowledge-fs-unstructured-sandbox.compose.yaml
├── middleware.env
├── nginx
│   ├── conf.d
│   ├── docker-entrypoint.sh
│   ├── https.conf.template
│   ├── nginx.conf.template
│   ├── proxy.conf.template
│   └── ssl
├── pgvector
│   └── docker-entrypoint.sh
├── ssrf_proxy
│   ├── docker-agent-entrypoint.sh
│   ├── docker-entrypoint.sh
│   ├── squid-agent.conf.template
│   ├── squid-common.conf.template
│   ├── squid.conf.template
│   ├── test_agent_ssrf_allowlist_unit.sh
│   └── test_ssrf_proxy_config.sh
├── startupscripts
│   ├── init.sh
│   └── init_user.script
├── tidb
│   ├── config
│   └── docker-compose.yaml
└── volumes
├── app
├── certbot
├── db
├── myscale
├── oceanbase
├── opensearch
├── plugin_daemon
├── redis
├── sandbox
└── weaviate
