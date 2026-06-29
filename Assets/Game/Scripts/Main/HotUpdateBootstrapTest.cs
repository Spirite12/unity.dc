using System;
using System.Collections.Generic;
using Cysharp.Threading.Tasks;
using DCFrame;
using UnityEngine;
using UnityEngine.AddressableAssets;
using UnityEngine.AddressableAssets.ResourceLocators;
using UnityEngine.ResourceManagement.AsyncOperations;

namespace Game {
    public class HotUpdateBootstrapTest : MonoBehaviour {
        private bool isRunning;

        private void Start() {
            RunHotUpdate().Forget();
        }

        /// <summary>
        /// 测试首包启动热更流程：先更新 Catalog，再下载 GameStartUp 标签资源。
        /// </summary>
        public async UniTask RunHotUpdate() {
            if (isRunning) {
                Debug.LogWarning("首包热更测试流程正在执行中。");
                return;
            }

            isRunning = true;
            try {
                Debug.Log("首包热更测试开始。");

                bool enableHotUpdate = await AAHotUpdate.LoadSettings();
                if (!enableHotUpdate) {
                    Debug.Log("未开启热更配置，跳过首包热更测试流程。");
                    return;
                }

                if (!await UpdateCatalogs()) {
                    Debug.LogError("Catalog 更新失败，停止首包热更测试流程。");
                    return;
                }

                await DownloadStartupAssets();
                Debug.Log("首包热更测试完成。");
            }
            catch (Exception ex) {
                Debug.LogException(ex);
            }
            finally {
                isRunning = false;
            }
        }

        /// <summary>
        /// 检查并更新 Addressables Catalog，确保后续能读取最新远端配置。
        /// </summary>
        private async UniTask<bool> UpdateCatalogs() {
            AsyncOperationHandle<List<string>> checkHandle = Addressables.CheckForCatalogUpdates(false);
            await checkHandle.Task;
            if (checkHandle.Status != AsyncOperationStatus.Succeeded) {
                Debug.LogError("检查 Catalog 更新失败。");
                Addressables.Release(checkHandle);
                return false;
            }

            List<string> catalogs = checkHandle.Result;
            if (catalogs == null || catalogs.Count == 0) {
                Debug.Log("Catalog 已是最新。");
                Addressables.Release(checkHandle);
                return true;
            }

            foreach (var item in catalogs) {
                Debug.Log(item);
            }
            Debug.Log($"发现 {catalogs.Count} 个 Catalog 需要更新。");
            AsyncOperationHandle<List<IResourceLocator>> updateHandle = Addressables.UpdateCatalogs(true, catalogs, false);
            await updateHandle.Task;
            bool isSuccess = updateHandle.Status == AsyncOperationStatus.Succeeded;
            if (!isSuccess) {
                Debug.LogError("更新 Catalog 失败。");
            }

            Addressables.Release(updateHandle);
            Addressables.Release(checkHandle);
            return isSuccess;
        }

        /// <summary>
        /// 下载标记为 GameStartUp 的启动前热更资源。
        /// </summary>
        private static async UniTask<bool> DownloadStartupAssets() {
            long size = await AAHotUpdate.GetStartupDownloadSize();
            Debug.Log($"启动前资源下载大小：{FormatBytes(size)}");
            if (size <= 0) {
                return true;
            }

            bool isSuccess = await AAHotUpdate.DownloadStartup();
            Debug.Log(isSuccess ? "启动前资源下载完成。" : "启动前资源下载失败。");
            return isSuccess;
        }

        /// <summary>
        /// 将字节数转换为方便阅读的显示文本。
        /// </summary>
        private static string FormatBytes(long bytes) {
            if (bytes <= 0) {
                return "0 B";
            }

            string[] units = { "B", "KB", "MB", "GB" };
            double value = bytes;
            int unitIndex = 0;
            while (value >= 1024 && unitIndex < units.Length - 1) {
                value /= 1024;
                unitIndex++;
            }

            return $"{value:0.##} {units[unitIndex]}";
        }
    }
}
