using UnityEngine;
using System.Collections;

namespace CS.AudioToolkit
{
    public class StopAudio : AudioTriggerBase
    {
        public string audioID;
        public float fadeOut = 0;

        protected override void _OnEventTriggered()
        {
            AudioController.Stop( audioID, fadeOut );
        }
    }
}