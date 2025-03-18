using UnityEngine;
using System.Collections;

namespace CS.AudioToolkit
{
    public class PauseAllAudio : AudioTriggerBase
    {
        public enum PauseType
        {
            All = 0,
            MusicOnly = 1,
            AmbienceOnly = 2,
            Category = 3,
        }

        public PauseType pauseType = PauseType.All;
        public float fadeOut = 0;
        public string categoryName;

        protected override void _OnEventTriggered()
        {
            switch( pauseType )
            {
            case PauseType.All:
                AudioController.PauseAll( fadeOut ); break;
            case PauseType.MusicOnly:
                AudioController.PauseChannel( AudioChannelType.Music, fadeOut ); break;
            case PauseType.AmbienceOnly:
                AudioController.PauseChannel( AudioChannelType.Ambience, fadeOut ); break;
            case PauseType.Category:
                AudioController.PauseCategory( categoryName, fadeOut ); break;
            }
        }
    }
}