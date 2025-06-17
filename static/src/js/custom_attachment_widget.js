/** @odoo-module **/

import { Component, useState } from '@odoo/owl';
import { registry } from '@web/core/registry';

class CustomAttachmentWidget extends Component {
    setup() {
        this.state = useState({
            attachment: this.props.value || '',
            attachmentType: this.props.record && this.props.record.data ? this.props.record.data.attachment_type : '',
        });
    }

    get isImage() {
        return this.state.attachmentType && this.state.attachmentType.startsWith('image');
    }

    get isVideo() {
        return this.state.attachmentType && this.state.attachmentType.startsWith('video');
    }

    get isAudio() {
        return this.state.attachmentType && this.state.attachmentType.startsWith('audio');
    }
}

CustomAttachmentWidget.template = 'ain.CustomAttachmentWidget';

registry.category('fields').add('custom_attachment_widget', CustomAttachmentWidget);
