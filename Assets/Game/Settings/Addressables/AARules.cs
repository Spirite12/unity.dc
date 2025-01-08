using System.Collections.Generic;
using UnityEngine;

public class AARules : ScriptableObject {
    
    [Header("以单资源打包（可以是资源，也可以是文件夹）")]
    public List<Object> singleList = new List<Object>();
    
    [Header("以标签打同一个包")]
    public List<HierarchyLabel> labelList = new List<HierarchyLabel>();
    
    [Header("以文件夹打包（文件夹之间没有关联）")]
    public List<HierarchyDir> folderList = new List<HierarchyDir>();

    [System.Serializable]
    public class HierarchyLabel {
        [Header("标签名称")]
        public string label = "";
        [Header("以单资源打包（可以是资源，也可以是文件夹）")]
        public List<Object> resList = new List<Object>();
    }        
        
    [System.Serializable]
    public class HierarchyDir {
        [Range(1, 5)]
        [Header("第几级文件夹")]
        public int number = 1;
        [Header("文件夹根路径")]
        public Object folderPath;
        [Header("过滤的文件夹")]
        public List<Object> excludePathList = new List<Object>();
    }
}