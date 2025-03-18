using UnityEngine;
using System.Collections;
using UnityEngine.Serialization;

namespace CS.AudioToolkit
{
    public class PlayAudio : AudioTriggerBase
    {
        public enum PlayPosition
        {
            Global,
            ChildObject,
            ObjectPosition,
        }

        public string audioID;
        
        [FormerlySerializedAs( "soundType" )]
        public AudioChannelType channel = AudioChannelType.Default;
        public PlayPosition position = PlayPosition.Global; 
        public float volume = 1;
        public float delay = 0;
        public float startTime = 0;

        override protected void Awake()
        {
            if ( triggerEvent == EventType.OnDestroy && position == PlayPosition.ChildObject )
            {
                position = PlayPosition.ObjectPosition;
                Debug.LogWarning( "OnDestroy event can not be used with ChildObject" );
            }
            base.Awake();
        }

        private void _Play()
        {
            switch ( position )
            {
            case PlayPosition.Global:
                AudioController.Play( audioID, volume, delay, startTime, channel ); break;
            case PlayPosition.ChildObject:
                AudioController.Play( audioID, transform, volume, delay, startTime, channel ); break;
            case PlayPosition.ObjectPosition:
                AudioController.Play( audioID, transform.position, null, volume, delay, startTime, channel ); break;
            }
        }

        protected override void _OnEventTriggered()
        {
            if ( string.IsNullOrEmpty( audioID ) ) return;
            _Play();
        }
    }

}