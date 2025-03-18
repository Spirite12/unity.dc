using UnityEngine;
using System.Collections;

namespace CS.AudioToolkit
{
    public class UnpauseAllAudio : AudioTriggerBase
    {
        public enum PauseType
        {
            All = 0,
            MusicOnly = 1,
            AmbienceOnly = 2,
            Category = 3,
        }

        public PauseType pauseType = PauseType.All;
        public float fadeIn = 0;
        public string categoryName;

        protected override void _OnEventTriggered()
        {
            switch ( pauseType )
            {
            case PauseType.All:
                AudioController.UnpauseAll( fadeIn ); break;
            case PauseType.MusicOnly:
                AudioController.UnpauseChannel( AudioChannelType.Music, fadeIn ); break;
            case PauseType.AmbienceOnly:
                AudioController.UnpauseChannel( AudioChannelType.Ambience, fadeIn ); break;
            case PauseType.Category:
                AudioController.UnpauseCategory( categoryName, fadeIn ); break;
            }
        }
    }
}