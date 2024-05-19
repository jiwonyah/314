from flask import Blueprint, request, g, jsonify, render_template, session
from csit314.entity.Review import Review
from csit314.entity.UserAccount import UserAccount
from .Form.WriteReviewForm import WriteReviewForm
from csit314.controller.role_service.decorators import login_required, buyer_seller_only, suspended

class BuyerSellerWriteReviewController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule("/write-review/<int:agent_id>", view_func=self.show_reviewForm_index, methods=['GET'])
        self.add_url_rule("/write-review/<int:agent_id>", view_func=self.write_review, methods=['POST'])
        self.add_url_rule("/agents", view_func=self.agent_list_index, methods=['GET'])
        self.add_url_rule("/api/agents", view_func=self.agent_list, methods=['GET'])

    @login_required
    @buyer_seller_only
    @suspended
    def show_reviewForm_index(self, agent_id):
        form = WriteReviewForm()
        user = UserAccount.query.get(agent_id)
        if user is None:
            return jsonify({'error': 'Agent not found'}), 404
        return render_template('review/writeReviewForm.html', agent_id=agent_id, form=form, user=user)

    @login_required
    @buyer_seller_only
    @suspended
    def write_review(self, agent_id):
        if request.is_json:
            json_data = request.get_json()
            form = WriteReviewForm(data=json_data)

            if form.validate_on_submit():
                details = {
                    'rating': json_data.get('rating'),
                    'content': json_data.get('content'),
                    'author_userid': g.user.userid,
                    'agent_id': agent_id
                }
                print(f"Details to be used for creating review: {details}")

                success = Review.createReview(details, agent_id)
                if success:
                    return jsonify({'success': True, 'message': 'Review is submitted successfully'}), 201
                else:
                    return jsonify({'success': False, 'error': 'Failed to submit review'}), 500
            else:
                errors = [{'field': field, 'message': ', '.join(error)} for field, error in form.errors.items()]
                print(f"Form validation errors: {errors}")
                return jsonify({'success': False, 'errors': errors}), 422
        else:
            return jsonify({'error': 'Request must be JSON'}), 415

    @suspended
    def agent_list_index(self):
        return render_template('review/agentListPage.html'), 200

    @suspended
    def agent_list(self):
        agents = UserAccount.query.filter_by(role='agent').all()
        if not agents:
            return jsonify({'error': 'No agents found'}), 404
        agent_data = [
            {
                'id': agent.id,
                'userid': agent.userid,
                'firstName': agent.firstName,
                'lastName': agent.lastName,
                'email': agent.email,
                'role': agent.role  # agent.role.value
            } for agent in agents
        ]
        return jsonify(agents=agent_data), 200


